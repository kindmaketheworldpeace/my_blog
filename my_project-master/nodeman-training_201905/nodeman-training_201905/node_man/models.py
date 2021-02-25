# -*- coding: utf-8 -*-

# version: 1.0.2

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
#

from __future__ import unicode_literals

import json
import random
import re

import time
from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext as _
from jsonfield import JSONField
from celery.result import AsyncResult

from common.log import logger
from node_man import constants as const
from node_man.component.cmdb import Business, GSEAgentApiModel
from node_man.component.esbclient import client, client_backend
from node_man.component.exceptions import ComponentCallError, NginxSettingError, GseSettingError
from node_man.constants import (JOB_MAX_RETRY, JOB_SLEEP_SECOND, JOB_SUCCESS,
                                StatusType, CodeType, NodeType, StepType, JobType,
                                AGENT_JOB_TUPLE, PLUGIN_JOB_TUPLE, JOB_TUPLE, TASK_TIMEOUT)
from node_man.utils.basic import now

IP_PATTERN = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")


class Host(models.Model):
    """主机配置信息"""

    bk_biz_id = models.CharField(max_length=45)
    bk_cloud_id = models.CharField(u'云区域ID', max_length=45)

    bk_supplier_account = models.CharField(u'服务商', max_length=45, default='0', null=True, blank=True)
    bk_supplier_id = models.CharField(u'服务商ID', max_length=45, default='0', null=True, blank=True)
    inner_ip = models.CharField(u'通信IP', max_length=45)
    outer_ip = models.CharField(u'级联IP', max_length=45, blank=True, null=True, default='')
    login_ip = models.CharField(u'登录IP', max_length=45, blank=True, null=True, default='')
    data_ip = models.CharField(u'数据IP', max_length=45, blank=True, null=True, default='')
    cc_ip_types = models.CharField(u'注册CMDB的IP类型', max_length=45, blank=True, null=True, default='')

    os_type = models.CharField(max_length=45, choices=const.OS_CHOICES, default='linux')
    node_type = models.CharField(u'节点类型', max_length=45, choices=const.NODE_CHOICES)
    auth_type = models.CharField(max_length=45, choices=const.AUTH_CHOICES,
                                 default=const.AuthType.PASSWORD)
    account = models.CharField(u'账户名', max_length=45, default='')
    password = models.CharField(u'密码', max_length=200, blank=True, null=True)
    port = models.IntegerField(u'端口', null=True, default=22)
    key = models.TextField(u'密钥内容', blank=True, null=True)
    has_cygwin = models.BooleanField(default=False)
    is_deleted = models.BooleanField(u'是否已删除', default=False)

    job_status = models.IntegerField(u'作业状态', choices=const.JOB_STATUS_CHOICES, default=0)
    agent_status = models.IntegerField(u'agent运行状态', choices=const.IPROC_STATE_CHOICES, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(u'agent更新时间', null=True, auto_now=False)

    def __unicode__(self):
        return "{}_{}_{}_{}".format(self.inner_ip, self.node_type, self.bk_biz_id, self.bk_cloud_id)

    def to_dict(self, attrs):
        """ 转换为dict格式"""
        return {
            attr: getattr(self, attr)
            for attr in attrs
        }

    def update_job_status(self, status):
        logger.info(u'更新agent的最新任务状态，状态为%s' % status)
        self.job_status = const.JOB_STATUS_TYPE_DICT[status]
        self.save()

    def update_agent_status(self, status):
        self.agent_status = status
        self.save()

    def get_last_job_object(self, object_type="agent"):
        _in_tuple = ()
        if object_type == "agent":
            _in_tuple = AGENT_JOB_TUPLE
        if object_type == "plugin":
            _in_tuple = PLUGIN_JOB_TUPLE
        if object_type == "all":
            _in_tuple = JOB_TUPLE
        jobs = self.job_result.all().filter(job__job_type__in=_in_tuple).exclude(
            job__job_type=JobType.UPDATE_AUTHINFO).order_by("-id")
        return jobs[0] if jobs.count() else None

    @classmethod
    def get_os_type(cls, host_info, bk_cloud_id):
        try:
            instance = cls.objects.get(inner_ip=host_info["conn_ip"], bk_cloud_id=bk_cloud_id, is_deleted=False)
            return instance.os_type
        except:
            return host_info.get("os_type") or const.OsType.LINUX

    @classmethod
    def get_other_bizs(cls, inner_ip, bk_biz_id, bk_cloud_id=0):
        return cls.objects.filter(inner_ip=inner_ip,
                                  is_deleted=False,
                                  bk_cloud_id=bk_cloud_id).exclude(
            bk_biz_id=bk_biz_id).values_list("bk_biz_id", flat=True)

    class Meta:
        verbose_name = u"主机信息"
        verbose_name_plural = u"主机信息"


class HostStatus(models.Model):
    """主机状态信息：agent/plugin"""

    host = models.ForeignKey('Host', related_name='status', null=True, blank=True)
    name = models.CharField(u"进程名称", max_length=45, default='gseagent')
    status = models.CharField(u"进程状态", max_length=45, choices=const.PROC_STATE_CHOICES,
                              default=const.ProcStateType.UNKNOWN)
    is_auto = models.CharField(u"是否托管", max_length=45, choices=const.AUTO_STATE_CHOICES,
                               default=const.AutoStateType.AUTO)
    version = models.CharField(u"进程版本", max_length=45, blank=True, null=True, default='')
    proc_type = models.CharField(u"进程类型", max_length=45, choices=const.PROC_CHOICES,
                                 default=const.ProcType.AGENT)

    def __unicode__(self):
        return "{}_{}_{}".format(self.host, self.name, self.status)

    @classmethod
    def get_random_alived_proxy(cls, bk_biz_id, bk_cloud_id):
        """随机取一台可用的Proxy，用于执行脚本"""
        return random.choice(cls.get_alived_proxy(bk_biz_id, bk_cloud_id))

    @classmethod
    def get_alived_proxy(cls, bk_biz_id, bk_cloud_id, dict_format=False):
        """查询业务指定云区域下的可用proxy"""

        alived_status = cls.objects.filter(
            host__bk_biz_id=bk_biz_id,
            host__bk_cloud_id=bk_cloud_id,
            host__is_deleted=False,
            host__node_type=const.NodeType.PROXY,
            proc_type=const.ProcType.AGENT,
            status=const.ProcStateType.RUNNING
        )

        if dict_format is True:
            return [host_status.host.to_dict(['inner_ip', 'outer_ip'])
                    for host_status in alived_status]

        return [host_status.host for host_status in alived_status]

    @classmethod
    def get_host_related_proxy_list(cls, host):
        """查询与指定主机关联的proxy列表"""

        # 待安装的proxy放到第一位
        proxy_list = [{'inner_ip': host.inner_ip, 'outer_ip': host.outer_ip}]
        # 追加其他可用的proxy
        for p in cls.get_alived_proxy(host.bk_biz_id, host.bk_cloud_id):
            if p.inner_ip != host.inner_ip:
                proxy_list.append({'inner_ip': p.inner_ip, 'outer_ip': p.outer_ip})
        return proxy_list

    class Meta:
        verbose_name = u"主机状态"
        verbose_name_plural = u"主机状态"


class Job(models.Model):
    """任务信息"""

    creator = models.CharField(u'操作人', max_length=45, default='')
    bk_supplier_account = models.CharField(u'服务商', max_length=45, default='', null=True, blank=True)
    bk_supplier_id = models.CharField(u'服务商ID', max_length=45, default='', null=True, blank=True)
    bk_biz_id = models.CharField(u'业务ID', max_length=45)
    bk_cloud_id = models.CharField(u'区域ID', max_length=45)
    job_type = models.CharField(u'作业类型', max_length=45, choices=const.JOB_CHOICES,
                                default=const.JobType.INSTALL_PROXY)
    start_time = models.DateTimeField(u'创建任务时间', auto_now_add=True)
    end_time = models.DateTimeField(u'任务结束时间', blank=True, null=True)
    task_id = models.CharField(u'关联的celery_id', max_length=45, blank=True, null=True)
    bk_job_id = models.CharField(u'关联的job_id', max_length=32, blank=True, null=True)

    is_canceled = models.BooleanField(u'是否被取消任务', default=False)
    global_params = models.TextField(u'全局运行参数', blank=True, null=True)

    def __unicode__(self):
        return "{}_{}_{}".format(self.creator, self.bk_biz_id, self.job_type)

    def destroy_task(self):
        if not self.hosts.filter(status__in=[StatusType.QUEUE, StatusType.RUNNING]).exists():
            return
        logger.info(u"终止任务 %s" % self.task_id)
        task = AsyncResult(self.task_id)
        self.revoke_task(task)
        self.hosts.filter(status__in=[StatusType.QUEUE, StatusType.RUNNING]).update(status=StatusType.FAILED,
                                                                                    err_code=CodeType.FORCE_STOP,
                                                                                    step=_(u'强制终止'))
        self.is_canceled = True
        self.save()

    def revoke_task(self, task):
        if task.children:
            for child in task.children:
                self.revoke_task(child)
        try:
            task.revoke(terminate=True)
        except Exception as exc:
            logger.warning("终止任务失败 %s" % exc)
            pass

    def log(self, content, level='user', job_task_id=None):

        """录入db和日志文件"""
        # content = u'[ {} - {} ]: {}'.format(self.bk_job_id, now().strftime('%Y.%m.%d/%H:%M:%S'), content)
        task_log = TaskLog.objects.create(level=level, content=content, job_id=self.pk)

        # 标记子任务id
        if job_task_id:
            task_log.job_task_id = job_task_id
            task_log.save()

        logger_level = 'info' if level == 'user' else level
        if callable(getattr(logger, logger_level, None)):
            getattr(logger, logger_level)(content)

    @property
    def job_status(self):
        """
        RUNNING/SUCCESS/FAILED/PARTIAL_SUCCESS
        :return:
        """

        if self.hosts.filter(status__in=[StatusType.RUNNING, StatusType.QUEUE]):
            return "RUNNING"

        if not self.hosts.filter(status=StatusType.FAILED).exists():
            return "SUCCESS"

        if self.hosts.filter(status=StatusType.SUCCESS).exists():
            return "PARTIAL_SUCCESS"

        return "FAILED"

    def get_job_tasks(self, filter_kwargs=None):
        """查询子任务"""
        if filter_kwargs is None:
            filter_kwargs = {}
        filter_kwargs.update(job_id=self.pk)
        return JobTask.objects.filter(**filter_kwargs)

    def get_job_hosts(self, filter_kwargs=None):
        """查询子任务关联的主机"""
        if filter_kwargs is None:
            filter_kwargs = {}
        return [job_task.host for job_task in self.get_job_tasks(filter_kwargs)]

    def create_start_plugin_task(self, plugin, hosts):
        """启动插件"""
        from node_man.serializers import GsePluginSerializer
        from node_man.backend.manage_plugin.once_tasks import manage_process

        host_list = []

        with transaction.atomic():
            job = Job.objects.create(
                creator=self.creator,
                bk_biz_id=self.bk_biz_id,
                bk_cloud_id=self.bk_cloud_id,
                job_type=const.JobType.START_PLUGIN,
                global_params=json.dumps({'plugin': GsePluginSerializer(plugin).data})
            )

            for host in hosts:
                host_list.append(host.inner_ip)
                JobTask.objects.create(job=job, host=host)

        celery_task = manage_process.apply_async((job.id,), kwargs={})

        job.update_task_id(str(celery_task.task_id))

        self.log('create start_plugin job for auto_launch plugin: {}, job_id={}, hosts={}'.format(
            plugin.name,
            job.id,
            host_list
        ))

        self.log('start_plugin task result will not display here, you can goto {} to check it'.format(
            '<a class="task-detail" href="#/task">Detail</a>')
        )

    def start_auto_launch_plugins(self):
        """查询任务执行成功的主机列表"""

        auto_launch_plugins = GsePluginDesc.get_auto_launch_plugins()

        hosts_success = self.get_job_hosts({
            'status': StatusType.SUCCESS
        })

        auto_launch_plugin_list = [plugin_item.name for plugin_item in auto_launch_plugins]
        hosts_success_list = [host.inner_ip for host in hosts_success]

        if not auto_launch_plugins:
            self.log('no auto launch plugins need to start for {}'.format(hosts_success_list))
            return False

        if not hosts_success:
            self.log('no host need to start auto launch plugins {}'.format(auto_launch_plugin_list))
            return False

        self.log('start auto launch plugins {} for: {}'.format(auto_launch_plugin_list, hosts_success_list))

        for plugin in auto_launch_plugins:
            self.create_start_plugin_task(plugin, hosts_success)

        return True

    def update_job_task_id(self, task_id):
        """更新所有子任务的ID为celery_id"""
        self.get_job_tasks().update(task_id=task_id)

    def update_task_id(self, celery_id):
        """更新作业的任务ID为celery_id"""
        self.task_id = celery_id
        self.save()

    def update_bk_job_id(self, bk_job_id):
        """更新作业的任务ID为作业ID"""
        self.bk_job_id = bk_job_id
        self.save()

    def update_job_result(self, result):
        """
        更新作业中结果列表agent安装状态
        """
        for k, v in result.iteritems():
            try:
                job_task = JobTask.objects.get(job=self, host__inner_ip=k)
            except JobTask.DoesNotExist:
                self.log('can not find job_task of %s' % k, 'error')
                continue

            if v.get('status') == StatusType.SUCCESS:
                job_task.update_step(StepType.SCRIPT_DONE)
            else:
                job_task.update_status(v.get('status'),
                                       v.get('err_code'),
                                       v.get('err_desc'), StepType.OVER_FAILED)

    def update_status(self, status, err_code=None, err_desc=None, step=None, update_task=True, filter_kwargs={}):
        """
        更新作业中所有agent安装状态，和错误码
        """
        kwargs = {'status': status}
        if err_code:
            kwargs.update(err_code=err_code)
        if err_desc:
            kwargs.update(err_desc=err_desc)
        if status in [StatusType.FAILED, StatusType.SUCCESS]:
            kwargs.update(end_time=now())
        if status == StatusType.SUCCESS:
            step = StepType.OVER_SUCCESS
        elif status == StatusType.FAILED:
            step = StepType.OVER_FAILED

        if update_task:
            # 先更新状态，需要用步骤过滤，待优化
            self.get_job_tasks(filter_kwargs).update(**kwargs)

        # 后更新步骤
        if step:
            self.update_job_step(step, filter_kwargs)

    def update_job_step(self, step, filter_kwargs={}):
        """
        更新作业中所有agent安装步骤
        """
        for job_task in self.get_job_tasks(filter_kwargs):
            job_task.update_step(step)

    def register_host_to_cmdb(self, job_task=None):
        """
        反写主机信息到配置平台
        """
        # API
        job_tasks = None
        if job_task:
            hosts = [job_task.host.inner_ip]
            job_task.update_step(StepType.REGISTER_CMDB)
        else:
            self.update_job_step(StepType.REGISTER_CMDB, {'step': StepType.SCRIPT_DONE})
            job_tasks = self.get_job_tasks({'step': StepType.REGISTER_CMDB})
            hosts = [task.host.inner_ip for task in job_tasks]
        try:
            result, register_data = Business(bk_biz_id=self.bk_biz_id).add_host_to_resource(
                self.bk_cloud_id, hosts, self.bk_supplier_id)
        except ComponentCallError as e:
            e.record_transaction(self.log)
            return False, e.message
        if not result:
            return False, register_data

        # 注册成功的时候，直接在这里处理
        failed_count = 0
        for item in register_data:
            try:
                task = job_task or job_tasks.get(host__inner_ip=item["bk_host_innerip"])
            except:
                continue
            if item["result"]["status"] == StatusType.FAILED:
                failed_count += 1
                task.update_status(status=item["result"]["status"],
                                   err_code=CodeType.REGISTER_FAILED,
                                   err_desc=item["result"]["err_desc"])

            task.log(u'registered to cmdb %s: %s' % (item["result"]["status"].lower(), item["result"]["err_desc"]))
        if failed_count:
            # 当存在某些失败的时候，直接返回false agent和proxy每次仅注入一个，若失败，则全部失败
            # 云区域pagent如果有部分失败，整体任务来说也是失败，在外层对日志打印做下参数区分
            return False, 'Partially failed'
        return True, 'success'

    def auto_launch_plugin(self):
        """自动注册并启动插件，全部成功时：result=True
        # NB! 一开始考虑目前one_tasks中的任务不能复用在安装agent时创建的job及job_task，所以才
        会有这个函数，但是想了想，既然拉起插件是否成功不会影响到agent的安装结果，我决定换个思路：
        获取最终成功agent的主机列表及需要自动拉起的插件列表，然后重新创建job和job_task，最后以
        插件为单位，下发多个插件启动任务，并在日志中追加各个插件启动任务的链接，以实现逻辑解耦和
        代码复用.
        """

        raise NotImplementedError('如果产品一定要在agent安装环节显示插件操作的日志，请复活该函数！')

        def batch_register_plugins(plugin_names, hosts):
            """注册自动拉起的插件到gse，全部成功时：result=True"""
            return {
                'result': True,
                'success': {
                    'plugin1': ['1', '2', '3'],
                    'plugin2': ['1', '2', '3'],
                },
                'fail': {
                    'plugin1': ['11', '12', '13'],
                    'plugin2': ['11', '12', '13'],
                }
            }

        def batch_start_plugins(plugin_names, hosts):
            """启动插件，全部成功时：result=True"""
            return {
                'result': True,
                'success': {
                    'plugin1': ['1', '2', '3'],
                    'plugin2': ['1', '2', '3'],
                },
                'fail': {
                    'plugin1': ['11', '12', '13'],
                    'plugin2': ['11', '12', '13'],
                }
            }

        auto_launch_plugin_names = GsePluginDesc.get_auto_launch_plugins()

        # 先执行批量注册操作：[单插件+多IP] x 插件数 => 注册成功的插件(注册参数的子集): [单插件+多IP] x 插件数
        register_result = batch_register_plugins(auto_launch_plugin_names, ['1', '2', '3'])

        # 然后执行批量启动操作：[单插件+多IP] x 插件数 => 注册成功的插件(注册参数的子集): [单插件+多IP] x 插件数
        start_result = batch_start_plugins(['plugin1', 'plugin2'], ['1', '2', '3'])

        return {
            'result': register_result['result'] and start_result['result'],
            'data': {
                'register_result': register_result,
                'start_result': start_result
            }
        }

    def get_ijob_result(self, task_instance_id):
        """
        查询ijobs任务实例，获取ijobs任务的业务ID、步骤详情以及当前状态
        """

        # 查询作业
        try:
            task_info = client.job.get_task_result({'task_instance_id': task_instance_id})
        except ComponentCallError as e:
            e.record_transaction(self.log)
            self.log(u'【%s】call job api(get_task_result) error, detail：%s' % (task_instance_id, e))
            return False, False, e.message

        is_ok, is_finished, err_desc = False, task_info.get('isFinished'), ''
        # self.log(u'task_instance_id: %s, res: %s' % (task_instance_id, task_info), 'info')

        if is_finished:
            self.log(u'【%s】job finished.' % task_instance_id)
            task_instance = task_info.get('taskInstance', {})
            status = task_instance.get('status', 0)  # 作业状态, 2=run, 3=success, 4=fail
            is_ok = (status == JOB_SUCCESS)

        if is_finished and not is_ok:
            # err_desc = task_info['blocks'][0]['stepInstances'][0]['stepIpResult'][0]['resultTypeText']
            err_log = self.get_job_log()
            err_desc = err_log.get('logContent')
            self.log('job failed: %s' % err_desc)

        return is_finished, is_ok, err_desc

    def poll_job_result(self, task_id, max_retries=JOB_MAX_RETRY, sleep_time=JOB_SLEEP_SECOND):
        """
        轮询ijobs任务，返回任务执行的结果，和状态码
        """

        retries = 0
        while retries <= max_retries:
            self.log(u'【%s】waiting for job finished（%s/%s）' % (task_id, retries, max_retries))
            is_finished, is_ok, err_desc = self.get_ijob_result(task_id)

            # 等待执行完毕
            if not is_finished:
                retries += 1
                time.sleep(sleep_time)
                continue

            # 执行成功
            if is_ok:
                self.log(u'【%s】job execute success' % task_id)
                return StatusType.SUCCESS, CodeType.SUCCESS, 'success'

            # 执行失败
            self.log(u'【%s】job execute failed' % task_id, 'warning')
            return StatusType.FAILED, CodeType.IJOBS_FAILED, err_desc

        # 执行超时
        if retries > max_retries:
            self.log(u'【%s】job execute timeout' % task_id)
            return StatusType.FAILED, CodeType.JOB_TIMEOUT, 'job execute timeout'

    def get_job_log(self):
        """
        查询作业日志，分析结果
        """
        try:
            data = client.job.get_task_ip_log({'task_instance_id': self.bk_job_id})
        except ComponentCallError as e:
            e.record_transaction(logger.error)
            logger.error(u'get_job_log(ComponentCallError): %s' % e)
            return {
                'result': False,
                'logContent': e.message
            }

        # 解析日志
        try:
            log_content = data[0].get('stepAnalyseResult')[0].get('ipLogContent')[0].get('logContent')
            return {
                'result': True,
                'logContent': log_content
            }
        except Exception as e:
            logger.error(u'get_job_log(Exception): %s' % e)
            return {
                'result': False,
                'logContent': e.message
            }

    def remove_hosts(self):
        for host in self.get_job_hosts():
            host.is_deleted = True
            host.save()

    def poll_agent_status(self, expected_status=1, need_remove=False, job_task_id=None):
        """
        轮询agent状态
        """

        retries = 0

        # agent状态查询接口参数

        while retries < JOB_MAX_RETRY:
            retries += 1
            try:
                hosts = self.get_job_hosts({'step': StepType.WAIT_AGENT})
                if hosts:
                    host_status = GSEAgentApiModel.get_agent_status_and_info({
                        "bk_supplier_id": int(self.bk_supplier_id) if self.bk_supplier_id else 0,
                        "hosts": [
                            {
                                'ip': host.inner_ip,
                                'bk_cloud_id': self.bk_cloud_id
                            }
                            for host in hosts]
                    })
                else:
                    self.log(u'check agent status finished：operate success', 'user', job_task_id)
                    break
            except ComponentCallError as e:
                e.record_transaction(self.log, 'user', job_task_id)
                # 查询出错，继续重试
                self.log(u'query agent status failed: %s' % e.message, 'user', job_task_id)
                self.update_status(StatusType.FAILED, CodeType.WAIT_AGENT_FAILED,
                                   filter_kwargs={'step': StepType.WAIT_AGENT})
                return False

            # self.log(u'query agent status: kwargs=%s, res=%s' % (kwargs, host_status))
            status_list = []
            for plat_host, status in host_status.iteritems():
                bk_cloud_id, inner_ip = plat_host.split(':')

                # 安装成功或卸载成功
                if status.get('bk_agent_alive') == expected_status:
                    self.update_status(StatusType.SUCCESS, CodeType.SUCCESS,
                                       filter_kwargs={'host__inner_ip': inner_ip})
                    # agent卸载后，移除主机
                    if expected_status == 0 and need_remove:
                        Host.objects.filter(inner_ip=inner_ip,
                                            bk_biz_id=self.bk_biz_id,
                                            bk_cloud_id=self.bk_cloud_id).update(is_deleted=True)
                # 无条件更新主机状态
                HostStatus.objects.filter(
                    host__inner_ip=inner_ip,
                    host__bk_biz_id=self.bk_biz_id,
                    host__bk_cloud_id=self.bk_cloud_id
                ).update(
                    status=const.PROC_STATUS_DICT.get(status.get('bk_agent_alive'), 'UNKNOWN'),
                    version=status.get('version')
                )

                status_list.append(status.get('bk_agent_alive'))

            self.log(u'agent status(%s/%s)(bk_agent_alive: 1->alive, 0->dead)：%s' %
                     (retries, JOB_MAX_RETRY, json.dumps(host_status, indent=2)), 'info', job_task_id)

            # agent全部上线，退出轮询
            if all(map(lambda x: x == expected_status, status_list)):
                self.log(u'check agent status finished：operate success', 'user', job_task_id)
                break

            self.log(u'check agent status(%s/%s)(bk_agent_alive: 1->alive, 0->dead): %s' % (
                retries,
                JOB_MAX_RETRY,
                status_list), 'user', job_task_id)

            time.sleep(JOB_SLEEP_SECOND)
        else:
            self.update_status(StatusType.FAILED, CodeType.JOB_TIMEOUT,
                               filter_kwargs={'step': StepType.WAIT_AGENT})
            self.log(u'query agent status timeout，give up, install failed.', 'user', job_task_id)

    def parse_job_result(self):
        """
        解析批量安装作业执行结果
        """

        # 初始化安装结果，默认为失败
        result = {
            job_host.inner_ip: {
                'id': job_host.id,
                'status': StatusType.FAILED,
                'err_desc': '',
                'err_code': CodeType.INSTALL_FAILED,
            }
            for job_host in self.get_job_hosts()}

        # 查询结果日志
        task_log = self.get_job_log()

        log_content = task_log.get('logContent')
        self.log(log_content)

        # 解析安装结果
        success_list = []
        for line in log_content.split('\n'):
            # 错误结果日志 ip step done
            if line.find("setup done") != -1:
                try:
                    ip = IP_PATTERN.findall(line)[0]
                except IndexError:
                    self.log("No IP found in line: {}".format(line))
                    continue
                status, err_code, err_desc = StatusType.SUCCESS, CodeType.SUCCESS, 'INSTALL_SUCCESS'
                success_list.append({'inner_ip': ip, 'outer_ip': ''})
            # 正确结果日志 xx.xx.xx.xx step failed -- failed info
            elif line.find("setup failed") != -1:
                try:
                    ip = IP_PATTERN.findall(line)[0]
                except IndexError:
                    self.log("No IP found in line: {}".format(line))
                    continue
                status, err_code, err_desc = StatusType.FAILED, CodeType.INSTALL_FAILED, line.split('--')[1]
            else:
                continue

            # 解析到无效IP
            if ip not in result:
                continue

            result[ip].update(status=status, err_code=err_code, err_desc=err_desc)
            self.log(u'job log parse result：\nip=%s, code=%s, desc=%s' % (ip, status, err_desc))

        return {
            'success_list': success_list,
            'result': result
        }

    class Meta:
        verbose_name = u"任务信息"
        verbose_name_plural = u"任务信息"


class JobTask(models.Model):
    """主机和任务关联表，存储任务详情及结果"""

    job = models.ForeignKey(Job, related_name='hosts', help_text=u'对应的作业信息')
    host = models.ForeignKey(Host, related_name='job_result', help_text=u'对应的主机信息')
    status = models.CharField(max_length=45, choices=const.STATUS_CHOICES,
                              default=const.StatusType.QUEUE)
    err_code = models.CharField(max_length=45, choices=const.CODE_CHOICES,
                                default=const.CodeType.INIT)
    err_desc = models.CharField(max_length=255, default='')
    task_id = models.CharField(u'对应的celery任务id', max_length=45, blank=True, null=True)
    step = models.CharField(max_length=45, choices=const.STEP_CHOICES,
                            default=const.StepType.INIT)
    step_index = models.IntegerField(u'步骤序号', default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{}_{}_{}".format(self.job, self.host, self.status)

    def log(self, content, level='user', flag=const.FlagType.EMPTY):
        """录入db和日志文件"""
        # content = u'[ {} - {} ]: {}'.format(self.host.inner_ip, now().strftime('%Y.%m.%d/%H:%M:%S'), content)
        logger_level = 'info' if level == 'user' else level
        try:
            TaskLog.objects.create(level=level, content=content, flag=flag,
                                   job_task_id=self.pk, job_id=self.job.pk)
        except Exception:
            logger.error("Failed to put log in db: {}".format(content))
            logger_level = 'error'
        if callable(getattr(logger, logger_level, None)):
            getattr(logger, logger_level)(content)

    def update_status(self, status, err_code=None, err_desc=None, step=None):
        """更新任务状态和错误码及描述"""
        self.status = status
        if err_desc:
            self.err_desc = err_desc
        if err_code:
            self.err_code = err_code
        if status == StatusType.SUCCESS:
            step = StepType.OVER_SUCCESS
            self.err_code = CodeType.SUCCESS
        elif status == StatusType.FAILED:
            step = StepType.OVER_FAILED
        if step:
            self.update_step(step)
        if self.host:
            self.host.update_job_status(status)
        self.save()

    def update_step(self, step):
        """更新任务步骤状态"""
        self.step_index += 1

        # 插入步骤描述日志
        if step not in [StepType.OVER_SUCCESS, StepType.OVER_FAILED] and step:
            self.log(step, flag=const.FlagType.STEP)
        self.step = step
        self.save()

    def update_task_id(self, task_id):
        """更新子任务的ID为celery_id"""
        self.task_id = task_id
        self.save()

    def poll_agent_status(self, expected_status=1):
        retries = 0
        # agent状态查询接口参数

        while retries < JOB_MAX_RETRY:
            retries += 1
            try:
                host_status = GSEAgentApiModel.get_agent_status_and_info({
                    "bk_supplier_id": int(self.job.bk_supplier_id) if self.job.bk_supplier_id else 0,
                    "hosts": [
                        {
                            'ip': self.host.inner_ip,
                            'bk_cloud_id': self.host.bk_cloud_id
                        }]
                })
            except ComponentCallError as e:
                # 查询出错，继续重试
                e.record_transaction(self.log, 'user')
                self.log(u'query agent status failed: %s' % e.message, 'user')
                self.update_status(StatusType.FAILED, CodeType.WAIT_AGENT_FAILED)
                return False
            # 安装成功
            current_status = 0
            for plat_host, status in host_status.iteritems():
                current_status = status.get('bk_agent_alive')
                HostStatus.objects.filter(host=self.host,
                                          proc_type=const.ProcType.AGENT,
                                          name="gseagent"
                                          ).update(
                    status=const.PROC_STATUS_DICT.get(status.get('bk_agent_alive'), 'UNKNOWN'),
                    version=status.get('version')
                )
                if status.get('bk_agent_alive') == expected_status and plat_host == ":".join(
                        [self.host.bk_cloud_id, self.host.inner_ip]):
                    self.update_status(StatusType.SUCCESS, CodeType.SUCCESS)
                    break

            if self.step != const.StepType.WAIT_AGENT:
                self.log(u'check agent status finished：operate success', 'user')
                break
            self.log(u'check agent status(%s/%s)(bk_agent_alive: 1->alive, 0->dead): %s' % (
                retries,
                JOB_MAX_RETRY, current_status), 'user')
            time.sleep(JOB_SLEEP_SECOND)
        else:
            self.update_status(StatusType.FAILED, CodeType.JOB_TIMEOUT)
            self.log(u'query agent status timeout，give up, install failed.', 'user')

    class Meta:
        verbose_name = u"任务详情"
        verbose_name_plural = u"任务详情"


class TaskLog(models.Model):
    """任务日志"""

    level = models.CharField(max_length=45, choices=const.LEVEL_CHOICES,
                             default=const.LevelType.user)
    content = models.TextField()
    flag = models.CharField(u'额外标记', max_length=45,
                            choices=const.FLAG_CHOICES, default=const.FlagType.EMPTY)
    create_time = models.DateTimeField(auto_now_add=True)
    job_task_id = models.IntegerField(u"关联的JobTask", null=True, blank=True)
    job_id = models.IntegerField(u"关联的Job", null=True, blank=True)

    def __unicode__(self):
        return "{}_{}_{}_{}".format(self.level, self.create_time, self.job_task_id, self.content)

    class Meta:
        verbose_name = u"任务日志"
        verbose_name_plural = u"任务日志"
        ordering = ("-id",)


class Cloud(models.Model):
    """云区域信息"""
    bk_cloud_id = models.CharField(max_length=45)
    bk_cloud_name = models.CharField(max_length=45)
    bk_supplier_id = models.CharField(max_length=45)
    creator = models.CharField(max_length=45, blank=True, null=True)
    bk_biz_id = models.CharField(max_length=45, blank=True, null=True)

    is_visible = models.BooleanField(u'是否可见', default=True)
    is_deleted = models.BooleanField(u'是否删除', default=False)

    def __unicode__(self):
        return "{}_{}_{}".format(self.bk_biz_id, self.bk_cloud_id, self.bk_cloud_name)

    @staticmethod
    def is_default_cloud(bk_cloud_id):
        return bk_cloud_id == const.DEFAULT_CLOUD

    @classmethod
    def is_existed_cloud(cls, bk_cloud_id, bk_biz_id):
        return cls.objects.filter(bk_cloud_id=bk_cloud_id, bk_biz_id=bk_biz_id).exists()

    @classmethod
    def is_existed_cloud_name(cls, bk_cloud_name, bk_biz_id):
        return cls.objects.filter(bk_cloud_name=bk_cloud_name, bk_biz_id=bk_biz_id, is_deleted=False).exists()

    @classmethod
    def get_cloud_name(cls, bk_cloud_id, bk_biz_id, bk_supplier_id='0'):
        try:
            instance = cls.objects.get(bk_cloud_id=bk_cloud_id,
                                       bk_biz_id=bk_biz_id,
                                       bk_supplier_id=bk_supplier_id)
            return instance.bk_cloud_name
        except cls.DoesNotExist:
            return u"未知"

    @classmethod
    def cache_all_cloud(cls):
        created_clouds, updated_clouds = [], []
        try:
            data = client_backend.cc.get_plat_id()
        except Exception as err:
            logger.error("Can not get cloud area info from cc: {}".format(str(err)))
            data = []

        for plat in data:
            try:
                obj, created = cls.objects.update_or_create(
                    defaults={
                        'bk_cloud_name': plat['platName'],
                        'creator': 'system',

                    },
                    **{
                        'bk_cloud_id': plat['platId'] if plat['platId'] else "0",
                        'bk_biz_id': '-1',
                        'bk_supplier_id': plat['platCompany'] if plat['platCompany'] else "0",
                    }
                )
            except:
                continue

            if created:
                created_clouds.append(plat['platId'])
            else:
                updated_clouds.append(plat['platId'])

        print """
======== clouds info ========
created: {}
updated: {}
======== clouds info ========""".format(
            created_clouds, updated_clouds
        )

    def destroy(self):
        self.is_deleted = True
        self.save()

    def disvisible(self):
        self.is_visible = False
        self.save()

    def envisible(self):
        self.is_visible = True
        self.save()

    def rename(self, new_name):
        self.bk_cloud_name = new_name
        self.save()

    class Meta:
        verbose_name = u"云区域信息"
        verbose_name_plural = u"云区域信息"


class Profile(models.Model):
    """个人资料补充信息"""
    bk_token = models.CharField(max_length=45)
    bk_user = models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, help_text=u'关联用户')
    favorite = JSONField(u"用户收藏信息，比如云区域等")

    def __unicode__(self):
        return "{}_{}".format(self.bk_user, self.bk_token)

    class Meta:
        verbose_name = u"个人资料"
        verbose_name_plural = u"个人资料"


class KV(models.Model):
    """
    配置表
    """
    key = models.CharField(u"键", max_length=255, db_index=True, primary_key=True)
    v_json = JSONField(u"值")

    def get_attr(self, attr):
        return self.v_json.get(attr)

    def set_attr(self, attr, val):
        self.v_json.update({attr: val})
        self.save()

    def __unicode__(self):
        return "{}_{}".format(self.key, self.v_json)

    @classmethod
    def get_nginx_config(cls, attr=None):
        """获取nginx配置"""
        NGINX = cls.objects.get(key='nginx')

        if attr:
            attr_url = NGINX.get_attr(attr)
            if not attr_url:
                raise NginxSettingError(u'%s is empty' % attr)
            return attr_url
        return NGINX

    @classmethod
    def get_gse_config(cls, attr=None):
        """获取nginx配置"""
        try:
            gse = cls.objects.get(key='gse')
        except Exception as err:
            logger.info("gse is not configured: {}".format(err))
            return ""

        if attr:
            attr_ip = gse.get_attr(attr)
            return attr_ip if attr_ip else ""
        return gse

    @classmethod
    def get_timeout_config(cls, attr="timeout"):
        """获取timeout配置"""
        try:
            return int(cls.objects.get(key=attr).get_attr(attr))
        except Exception as e:
            logger.error(u"获取任务超时配置信息异常：%s" % e)
            return TASK_TIMEOUT

    @classmethod
    def get_plugin_config(cls, attr="plugin_config"):
        """获取插件配置历史信息"""
        try:
            return cls.objects.get(key=attr).v_json
        except Exception as e:
            return {
                'user': '',
                'time': '未配置'
            }

    class Meta:
        verbose_name = u"配置表"
        verbose_name_plural = u"配置表"


class IP(models.Model):
    """
    机器信息
    """
    AUTH_TYPE = [(0, 'PASSWORD'), (1, 'KEY')]
    biz_id = models.CharField(u'业务id，用于过滤中转机', max_length=128)
    plat_id = models.CharField(u'所属云平台id', max_length=128)
    inner_ip = models.GenericIPAddressField(u'主机内网IP', max_length=128)
    outer_ip = models.GenericIPAddressField(u'主机外网IP', max_length=128, null=True, blank=True, default='')
    auth_type = models.SmallIntegerField(u'认证类型', default=0)
    err_code = models.SmallIntegerField(u'安装错误码', default=0)
    desc = models.CharField(u'错误描述', max_length=255, default='')
    status = models.SmallIntegerField(u'安装结果', default=0)
    type = models.SmallIntegerField(u'机器类型，proxy/agent', default=0)
    account = models.CharField(u'SSH登录用户', max_length=128)
    password = models.CharField(u'SSH登录密码', blank=True, max_length=128)
    port = models.IntegerField(u'SSH登录端口', default=22)
    create_time = models.DateTimeField(u'添加时间', auto_now_add=True)
    start_time = models.DateTimeField(u'任务开始时间', auto_now_add=True)
    end_time = models.DateTimeField(u'任务结束时间', null=True)
    is_public = models.BooleanField(u'是否共享', default=False)
    is_poped = models.BooleanField(u'是否弹出过错误信息', default=False)
    modify_status = models.SmallIntegerField(u'变更状态码', default=0)
    modify_type = models.SmallIntegerField(u'变更类型（卸载/刷新配置）', default=0)
    key = models.ForeignKey('SshKey', null=True, blank=True, help_text=u'SSH登录私钥')
    expiry_time = models.DateTimeField(u"密码或密钥失效时间", null=True)
    version = models.CharField(u'实时agent版本号（暂未启用）', max_length=128, blank=True, default='')
    os_type = models.CharField(u'操作系统类型', max_length=32,
                               choices=[('Windows', 'Windows'), ('Linux', 'Linux'), ('Aix', 'Aix')], default='Linux')
    has_cygwin = models.SmallIntegerField(u'是否有cygwin', choices=[(0, '没有'), (1, '有'), (2, '不需要')], default=0)
    exist = models.SmallIntegerField(u'实时agent状态（暂未启用）', default=0)

    managed = False

    def __unicode__(self):
        return u'%s-%s-%s' % (self.inner_ip, self.outer_ip, self.status)

    class Meta:
        ordering = ['is_public', '-create_time']
        verbose_name = u'IP信息'
        verbose_name_plural = u'IP信息'
        db_table = u'miya_ip'
        managed = False


class SshKey(models.Model):
    """
    密钥文件信息
    """
    key_name = models.CharField(u'密钥文件名', max_length=128)
    key_path = models.CharField(u'密钥文件路径', max_length=255)
    key_content = models.TextField(u'密钥文件内容', max_length=255)
    create_time = models.DateTimeField(u'上传时间', auto_now_add=True)

    def __unicode__(self):
        return u'%s-%s' % (self.key_name, self.create_time)

    class Meta:
        db_table = 'miya_sshkey'
        ordering = ['-create_time']
        verbose_name = u'密钥文件信息'
        verbose_name_plural = u'密钥文件信息'
        managed = False


class GsePluginDesc(models.Model):
    """
    插件信息表
    """
    name = models.CharField(u'插件名', max_length=32)
    description = models.CharField(u'插件描述', max_length=128)
    scenario = models.CharField(u'使用场景', max_length=256)
    description_en = models.CharField(u'英文插件描述', max_length=128, null=True, blank=True)
    scenario_en = models.CharField(u'英文使用场景', max_length=256, null=True, blank=True)
    category = models.CharField(u'所属范围', max_length=32, choices=const.CATEGORY_CHOICES)
    launch_node = models.CharField(u'宿主节点类型要求', max_length=32, choices=[
        ('agent', 'agent'),
        ('proxy', 'proxy'),
        ('all', 'all'),
    ], default="all")

    config_file = models.CharField(u'配置文件名称', max_length=128, null=True, blank=True)
    config_format = models.CharField(u'配置文件格式类型', max_length=32, choices=const.CONFIG_FILE_FORMAT_CHOICES,
                                     default='json', null=True, blank=True)

    use_db = models.BooleanField(u'是否使用数据库', default=0)
    auto_launch = models.BooleanField(u'是否在成功安装agent后自动拉起', default=False)
    is_binary = models.BooleanField(u'是否二进制文件', default=1)

    class Meta:
        verbose_name = u'插件信息表'
        verbose_name_plural = u'插件信息表'

    def __unicode__(self):
        return self.name

    @classmethod
    def get_auto_launch_plugins(cls):
        return cls.objects.filter(auto_launch=True)

    def get_package_by_os(self, os, pkg_name):
        package = Packages.objects.get(
            project=self.name, os=os, pkg_name=pkg_name,
            cpu_arch="x86_64"
        )
        return package

    def get_control_by_os(self, os):
        control = ProcControl.objects.get(project=self.name, os=os)
        return control


class Packages(models.Model):
    """
    插件更新包信息表
    """
    pkg_name = models.CharField(u'压缩包名', max_length=128)
    version = models.CharField(u'版本号', max_length=128)
    module = models.CharField(u'所属服务', max_length=32)
    project = models.CharField(u'工程名', max_length=32)
    pkg_size = models.IntegerField(u'包大小')
    pkg_path = models.CharField(u'包路径', max_length=128)
    md5 = models.CharField(u'md5值', max_length=32)
    pkg_mtime = models.CharField(u'包更新时间', max_length=48)
    pkg_ctime = models.CharField(u'包创建时间', max_length=48)
    location = models.CharField(u'安装包链接', max_length=512)
    os = models.CharField(u'系统类型', max_length=32, choices=const.PLUGIN_OS_CHOICES, default=const.PluginOsType.linux)
    cpu_arch = models.CharField(u'CPU类型', max_length=32, choices=const.CPU_CHOICES, default=const.CpuType.x86_64)

    class Meta:
        verbose_name = u'模块/工程安装包信息表'
        verbose_name_plural = u'模块/工程安装包信息表'

    def __unicode__(self):
        return "{}-{}".format(self.module, self.project)


class ProcControl(models.Model):
    """
    插件更新包信息表
    """
    module = models.CharField(u'模块名', max_length=32)
    project = models.CharField(u'工程名', max_length=32)

    install_path = models.CharField(u'安装路径', max_length=128)
    log_path = models.CharField(u'日志路径', max_length=128)
    data_path = models.CharField(u'数据文件路径', max_length=128)
    pid_path = models.CharField(u'pid文件路径', max_length=128)
    start_cmd = models.CharField(u'启动命令', max_length=128)
    stop_cmd = models.CharField(u'停止命令', max_length=128)
    restart_cmd = models.CharField(u'重启命令', max_length=128)
    reload_cmd = models.CharField(u'重载命令', max_length=128)
    kill_cmd = models.CharField(u'kill命令', max_length=128, default="")
    version_cmd = models.CharField(u'进程版本查询命令', max_length=128, default="")
    health_cmd = models.CharField(u'进程健康检查命令', max_length=128, default="")
    os = models.CharField(u'系统类型', max_length=32, choices=const.PLUGIN_OS_CHOICES, default=const.PluginOsType.linux)

    class Meta:
        verbose_name = u'模块/进程控制信息表'
        verbose_name_plural = u'模块/进程控制信息表'

    def __unicode__(self):
        return "{}-{}".format(self.module, self.project)
