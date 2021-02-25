# _*_ coding: utf-8 _*_
import json
import re
from django.utils.translation import ugettext as _
from django.db.models import Q
from rest_framework import serializers

from node_man.models import Host, Cloud, HostStatus, GsePluginDesc, ProcControl
from node_man.constants import (NodeType, OpType, OsType, JobType,
                                ProcStateType, StatusType, AuthType, TASK_TIMEOUT)
from node_man.component.cmdb import Business


class AgentTypeValidator(object):
    def __call__(self, value):
        if value.get("node_type", NodeType.AGENT) == NodeType.PROXY:
            if not value.get('os_type', OsType.LINUX) == OsType.LINUX:
                message = _(u'非linux机器无法安装proxy')
                raise serializers.ValidationError(message, code='node_type')
            if value.get("op_type") == OpType.INSTALL and not value.get("cascade_ip"):
                message = _(u'安装proxy必须要填写级联ip')
                raise serializers.ValidationError(message, code='node_type')


class HostExistValidator(object):
    def __init__(self, base=None):
        self.base = base

    def __call__(self, value):
        if self.base and self.base.bk_biz_id == value["bk_biz_id"] and value["op_type"] == OpType.INSTALL:
            message = _(u'%s:当前机器已经安装了AGENT') % self.base.inner_ip
            raise serializers.ValidationError(message, code='exist')
        if self.base is None and value["op_type"] not in [OpType.INSTALL, OpType.IMPORT]:
            message = _(u'%s:当前机器还未安装AGENT，不能做其他操作') % value["conn_ip"]
            raise serializers.ValidationError(message, code='exist')


class HostBelongsValidator(object):
    def __call__(self, value):
        # 校验IP是否为本业务下的ip get_biz_info_by_host(bk_cloud_id,inner_ip);
        # 不需要这个功能了，没有调用
        bk_cloud_id = value["bk_cloud_id"]
        inner_ip = value["conn_ip"]
        biz_info = Business.get_appid_by_host(inner_ip, bk_cloud_id, Business(value["bk_biz_id"]).bk_supplier_id)
        if biz_info is not None:
            if str(biz_info["bk_biz_id"]) != value['bk_biz_id']:
                message = _(u'%s:当前机器属于业务【%s】，请调整重试') % (inner_ip, biz_info["bk_biz_name"])
                raise serializers.ValidationError(message, code='exist')


class WindowsValidator(object):
    def __call__(self, value):
        if value.get('os_type') != OsType.WINDOWS and value.get('') is True:
            message = _(u'参数错误，非windwos机器不需要cygwin')
            raise serializers.ValidationError(message, code='cygwin')


class JobTypeValidator(object):
    def __call__(self, value):
        (op_type, agent_type) = tuple(value['job_type'].split("_"))
        hosts_count = len(value["hosts"])
        if agent_type == NodeType.PROXY and op_type == OpType.INSTALL:
            errors = []
            if 2 < Host.objects.filter(bk_cloud_id=value["bk_cloud_id"],
                                       bk_biz_id=value["bk_biz_id"],
                                       node_type=NodeType.PROXY,
                                       is_deleted=False).count() + hosts_count:
                errors.append(_(u'单个云区域最多只能安装2台PROXY'))
            if errors:
                raise serializers.ValidationError(errors, code='proxy_num')
        if agent_type == NodeType.PAGENT and not HostStatus.objects.filter(host__bk_cloud_id=value["bk_cloud_id"],
                                                                           host__bk_biz_id=value["bk_biz_id"],
                                                                           host__node_type=NodeType.PROXY,
                                                                           host__is_deleted=False,
                                                                           status=ProcStateType.RUNNING).exists():
            message = _(u'当前云区域没有可用的PROXY，请先检查并安装')
            raise serializers.ValidationError(message, code='not exist')


class CloudExistedValidator(object):
    def __call__(self, value):
        if not Cloud.is_existed_cloud(value["bk_cloud_id"], value["bk_biz_id"]) and not Cloud.is_default_cloud(
                value["bk_cloud_id"]):
            message = _(u'指定云区域不存在，请检查确认')
            raise serializers.ValidationError(message, code='not existed cloud')


class HostInstalledValidator(object):
    def __init__(self, ignore_installed_elsewhere=False):
        self.ignore_installed_elsewhere = ignore_installed_elsewhere

    def __call__(self, value):
        hosts = value['hosts']
        if not self.ignore_installed_elsewhere and len(hosts) > 0:
            installed_elsewhere = {}
            for host_instance in hosts:
                host = host_instance['host']
                inner_ip, bk_biz_id = [host[attr] for attr in ('conn_ip', 'bk_biz_id')]
                other_bizs = Host.get_other_bizs(inner_ip, bk_biz_id, value["bk_cloud_id"])
                if other_bizs:
                    installed_elsewhere[inner_ip] = map(str, other_bizs)
            if installed_elsewhere:
                raise serializers.ValidationError({'other_bk_biz_id': installed_elsewhere})


class HostJobStatusValidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if self.base is not None:
            jobs = self.base.job_result.all().exclude(job__job_type=JobType.UPDATE_AUTHINFO).order_by("-id")
            if jobs:
                last_job_result = jobs[0]
            else:
                return
            if value.get("op_type") in [OpType.UNINSTALL, OpType.REMOVE] and self.base.node_type == NodeType.PROXY:
                if Host.objects.filter(is_deleted=False,
                                       bk_cloud_id=value["bk_cloud_id"],
                                       bk_biz_id=value["bk_biz_id"],
                                       node_type=NodeType.PAGENT).exists():
                    message = _(u'当前云区域存在P-Agent,无法卸载Proxy')
                    raise serializers.ValidationError(message, code='node_type')
            if last_job_result.status in [StatusType.QUEUE, StatusType.RUNNING] and value[
                "op_type"] != JobType.UPDATE_AUTHINFO:
                message = _(u'当前机器[%s]正在执行操作过程中，请终止再操作') % self.base.inner_ip
                raise serializers.ValidationError(message, code='running')


class NodeTypeRelationValidator(object):
    def __call__(self, value):
        if value['job_type'] in [JobType.INSTALL_AGENT, JobType.REINSTALL_AGENT] \
                and not Cloud.is_default_cloud(value["bk_cloud_id"]):
            message = _(u'非直连区域，不能安装AGENT')
            raise serializers.ValidationError(message, code='default_cloud_id')
        if value['job_type'] in [JobType.INSTALL_PAGENT, JobType.INSTALL_PROXY, JobType.REINSTALL_PAGENT,
                                 JobType.REINSTALL_PROXY] \
                and Cloud.is_default_cloud(value["bk_cloud_id"]):
            message = _(u'直连区域，不能安装PROXY和PAGENT')
            raise serializers.ValidationError(message, code='default_cloud_id')


class AuthValidator(object):
    def __init__(self, base=None):
        self.base = base

    def __call__(self, value):
        if value["op_type"] in [OpType.INSTALL] or (self.base is not None and "account" in value):
            if not value.get("account"):
                message = _(u'%s：帐号信息为空，请确认') % value["conn_ip"]
                raise serializers.ValidationError(message, code='account_empty')
            if not value.get("port"):
                message = _(u'%s：SSH端口信息为空，请确认') % value["conn_ip"]
                raise serializers.ValidationError(message, code='port_empty')
            auth_type = value.get("auth_type", AuthType.PASSWORD)
            if auth_type == AuthType.PASSWORD and not (value.get("password")):
                message = _(u'%s：密码字段为空，请确认') % value["conn_ip"]
                raise serializers.ValidationError(message, code='password_empty')
            if auth_type == AuthType.KEY and not value.get("key"):
                message = _(u'%s：key字段为空，请确认') % value["conn_ip"]
                raise serializers.ValidationError(message, code='key_empty')
        elif self.base is not None and "account" not in value:
            auth_info = self.base.key if self.base.auth_type == AuthType.KEY else self.base.password
            if not (self.base.account and auth_info):
                message = _(u'%s：该IP的密码/密钥已过期(超过1天)') % value["conn_ip"]
                raise serializers.ValidationError(message, code='key_empty')


class BulkHostValidator(object):
    def __init__(self, hosts=None):
        self.hosts = hosts

    def __call__(self, value):
        errors = {}
        for host in self.hosts:
            if host.bk_cloud_id != value["bk_cloud_id"]:
                message = _(u'%s:当前机器属于%s云区域') % (
                    host.inner_ip, Cloud.get_cloud_name(host.bk_cloud_id, host.bk_biz_id, value["bk_supplier_id"]))
                errors[host.inner_ip] = message
                continue
            try:
                HostExistValidator(host)({"op_type": "INSTALL"})
            except serializers.ValidationError as exc:
                if isinstance(exc.detail, list):
                    exc.detail = exc.detail[0]
                errors[host.inner_ip] = exc.detail
        if errors:
            raise serializers.ValidationError([errors])


class CloudNameExistedValidator(object):
    def __init__(self, bk_biz_id=0):
        self.bk_biz_id = bk_biz_id

    def __call__(self, value):
        if Cloud.is_existed_cloud_name(value["bk_cloud_name"], self.bk_biz_id):
            raise serializers.ValidationError(_(u"已经存在相同的云区域，请修改后再提交"))


def url_validator(value):
    return True


def gse_ip_validator(value):
    ip_pattern = re.compile(
        r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")

    def is_valid(pattern, text):
        return pattern.match(text) is not None

    def check_format(ip, ip_type):
        if not ip:
            return None
        if not is_valid(ip_pattern, ip):
            raise serializers.ValidationError(_(u'{}:IP信息{}格式不正确'.format(ip_type, ip)), code="gse")

    check_format(value["v_json"].get("inner_ip", ""), "inner_ip")
    check_format(value["v_json"].get("outer_ip", ""), "outer_ip")


def timeout_validator(value):
    timeout = value["v_json"].get("timeout", "")

    try:
        timeout = int(timeout)
    except ValueError:
        pass

    if not isinstance(timeout, int) or timeout < TASK_TIMEOUT:
        raise serializers.ValidationError(
            _(u'超时配置信息({})格式不正确，请输入不小于{}的合法数字').format(timeout, TASK_TIMEOUT),
            code="timeout"
        )


class GlobalParmasExistValidator(object):

    def __init__(self):
        self.key = "global_params"

    def __call__(self, value):
        if not value.has_key(self.key):
            message = _(u'插件管理操作缺少global_parmas参数')
            raise serializers.ValidationError(message, code='running')


class PluginExistValidator(object):

    def __call__(self, instance):
        try:
            GsePluginDesc.objects.get(id=instance.get('id'), name=instance.get('name'))
        except GsePluginDesc.DoesNotExist, e:
            message = _(u'插件名称[%s]不在已安装的插件列表当中，请确定插件名称是否正确' % instance.get('name'))
            raise serializers.ValidationError(message, code='running')


class OsPluginValidator(object):

    def __call__(self, instance):

        global_params = instance.get("global_params")
        plugin = global_params.get("plugin").get("name")
        hosts = instance.get("hosts")
        os_hosts = {}
        for _host in hosts:
            host = Host.objects.get(is_deleted=False, **_host)
            os_hosts.setdefault(host.os_type, []).append(host)

        for os, hosts in os_hosts.iteritems():
            try:
                ProcControl.objects.get(project=plugin, os=os)
            except ProcControl.DoesNotExist, e:
                _hosts = [host.inner_ip for host in hosts]
                message = _(u'以下机器的操作系统(%s)无法安装此插件[%s]: %s，请重新选择机器' % (os, plugin, ",".join(_hosts)))
                raise serializers.ValidationError(message, code='running')
