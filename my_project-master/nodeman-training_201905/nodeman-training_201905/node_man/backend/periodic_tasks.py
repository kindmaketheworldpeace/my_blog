# -*- coding: utf-8 -*-
"""
celery任务入口
测试方法：设置celery_always_eager=True后启动测试，查看任务日志
遇到问题：测试中django创建的数据库，无法再celery中访问
"""
import datetime

from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Min

from common.log import logger
from node_man.component.cmdb import GSEAgentApiModel, Business
from node_man.component.gse import GSEAgent
from node_man.constants import (
    StepType, PROC_STATUS_DICT,
    StatusType, CodeType,
    ProcType, PLUGIN_STATUS_DICT, AUTO_STATUS_DICT
)
from node_man.models import Host, JobTask, HostStatus, GsePluginDesc
from requests_tracker.models import Record, Exclude


@periodic_task(run_every=(crontab(hour="*", minute="*/1", day_of_week="*", day_of_month="*", month_of_year="*")))
def get_agent_status_task():
    logger.info(u"get_agent_status_task:开始执行")
    # biz_list = Host.objects.filter(
    #     is_deleted=False
    # ).values("bk_biz_id").distinct()
    # bk_supplier_ids = {}
    # for biz in biz_list:
    #     bk_supplier_ids[biz["bk_biz_id"]] = Business(
    #         bk_biz_id=biz["bk_biz_id"]
    #     ).bk_supplier_id
    hosts = Host.objects.filter(is_deleted=False)
    params = {}
    hosts_dict = {}

    # 组装参数
    for host in hosts:
        try:
            bk_supplier_id = int(host.bk_supplier_id)
        except ValueError:
            continue
        hosts_dict["%s:%s" % (host.bk_cloud_id, host.inner_ip)] = host
        if bk_supplier_id in params:
            params[bk_supplier_id]["hosts"].append({
                "ip": host.inner_ip, "bk_cloud_id": host.bk_cloud_id
            })
        else:
            params[bk_supplier_id] = {
                "hosts": [{
                    "ip": host.inner_ip, "bk_cloud_id": host.bk_cloud_id
                }]
            }

    status_group_dict = {}

    # 状态分组
    for bk_supplier_id, param in params.iteritems():
        param.update({"bk_supplier_id": bk_supplier_id})
        all_agent_status = GSEAgentApiModel.get_agent_status_and_info(param)
        for key, value in all_agent_status.iteritems():
            host = hosts_dict.get(key)
            if host is None:
                continue
            host.update_agent_status(value["bk_agent_alive"])
            status_key = "{status}_{version}".format(
                status=PROC_STATUS_DICT[value["bk_agent_alive"]],
                version=value["version"])
            if status_key in status_group_dict:
                status_group_dict[status_key]["hosts"].append(host)
            else:
                status_group_dict[status_key] = {
                    "status": PROC_STATUS_DICT[value["bk_agent_alive"]],
                    "version": value["version"],
                    "hosts": [host]}

    # 更新到DB
    for key, value in status_group_dict.iteritems():
        status_objects = HostStatus.objects.filter(
            host__in=value["hosts"], name="gseagent")
        if status_objects.exists():
            status_objects.update(
                status=value["status"],
                version=value["version"]
            )
        for obj in status_objects:
            value["hosts"].pop(value["hosts"].index(obj.host))
            if not value["hosts"]:
                break
        instances = [
            HostStatus(
                host=host, status=value["status"], version=value["version"]
            ) for host in value["hosts"]
        ]
        HostStatus.objects.bulk_create(instances)


@periodic_task(run_every=(crontab(hour="*", minute="*/5", day_of_week="*", day_of_month="*", month_of_year="*")))
def clean_expired_info():
    """
    清楚一些过期的信息
    过期的账户信息
    超时的任务
    """
    # 清除过期的账户信息
    logger.info(u"清除过期的账户信息")
    Host.objects.filter(
        is_deleted=False,
        update_time__lte=datetime.datetime.now() - datetime.timedelta(days=1),
    ).exclude(key="", password="").update(key="", password="")

    # 清除超时的任务
    logger.info(u"清除超时的任务")
    JobTask.objects.filter(
        create_time__lte=datetime.datetime.now() - datetime.timedelta(minutes=30),
        status__in=[StatusType.QUEUE, StatusType.RUNNING]
    ).update(
        status=StatusType.FAILED,
        err_code=CodeType.JOB_TIMEOUT,
        step=StepType.OVER_FAILED,
        end_time=datetime.datetime.now()
    )

    # 检查组件请求记录，清空3天前的记录，每次最多删除300条
    three_days_before = datetime.datetime.now() - datetime.timedelta(days=3)
    try:
        min_id = Record.objects.all().aggregate(Min("id"))
        Record.objects.filter(
            date_created__lte=three_days_before,
            id__lte=min_id["id__min"] + 300
        ).order_by("id").delete()
        Exclude.objects.get_or_create(
            name='login_pattern', column=102, rule="*/login/*",
            is_active=1, category=1)
    except Exception, e:
        pass


@periodic_task(run_every=(crontab(hour="*", minute="*/5", day_of_week="*", day_of_month="*", month_of_year="*")))
def get_plugin_status_task():
    logger.info(u"get_plugin_status_task:开始执行")
    hosts = Host.objects.filter(is_deleted=False)
    biz_list = hosts.values("bk_biz_id").distinct()

    bk_supplier_ids = {}
    for biz in biz_list:
        bk_supplier_ids[biz["bk_biz_id"]] = Business(
            bk_biz_id=biz["bk_biz_id"]
        ).bk_supplier_id

    host_id_mapping = {}
    _hosts = {}
    # 组装参数
    for host in hosts:
        bk_supplier_id = bk_supplier_ids.get(host.bk_biz_id)
        if bk_supplier_id is None:
            continue

        _host = {
            "ip": host.inner_ip,
            "bk_supplier_id": int(bk_supplier_ids[host.bk_biz_id]),
            "bk_cloud_id": int(host.bk_cloud_id)
        }

        _key = "%s:%s:%s" % (
            host.inner_ip, bk_supplier_ids[host.bk_biz_id], host.bk_cloud_id)

        host_id_mapping[_key] = host

        if _hosts.has_key(bk_supplier_id):
            _hosts[bk_supplier_id].append(_host)
        else:
            _hosts[bk_supplier_id] = [_host]

    agent = GSEAgent()
    instances = []
    # 状态分组
    for plugin in get_plugin():
        for bk_supplier_id, hosts in _hosts.items():
            data = agent.get_proc_status(hosts, plugin)
            for row in data:
                host = row.get("host")
                flag = row.get("flag")
                status = PLUGIN_STATUS_DICT[row.get("status", 0)]
                is_auto = AUTO_STATUS_DICT[row.get("isauto", 0)]
                meta = row.get("meta")
                plugin_name = meta.get("name").strip()
                version = row.get("version").strip()

                _key = "%s:%s:%s" % (
                    host.get("ip"), host.get("bk_supplier_id"),
                    host.get("bk_cloud_id"))

                logger.info(u"plugin_status_update: %s %s value: %s", host.get("ip"), plugin_name, row)
                instance, created = HostStatus.objects.get_or_create(
                    host=host_id_mapping[_key], name=plugin_name,
                    proc_type=ProcType.PLUGIN
                )
                data = dict(
                    status=status, is_auto=is_auto, version=version
                )
                instance.__dict__.update(**data)
                instance.save()
    logger.info(u"get_plugin_status_task:执行完成")


def get_plugin():
    plugins = GsePluginDesc.objects.filter(category='official')
    for plugin in plugins:
        yield plugin.name
