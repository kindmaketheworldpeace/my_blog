# -*- coding: utf-8 -*-
import re

from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.http import Http404, HttpResponseNotAllowed, StreamingHttpResponse
from django.utils.translation import ugettext as _

import settings
from blueking.component.client import ComponentClient
from node_man.component.cmdb import Business, APIModel
from node_man.component.esbclient import client_v2
from node_man.component.gse import GSEAgent
from node_man.models import Cloud, KV, Host, GsePluginDesc, Job, HostStatus
from node_man.component.viewsets import ModelViewSet
from node_man.serializers.misc import CloudSerializer, KvSerializer
from node_man.serializers.validators import gse_ip_validator
from node_man.component.exceptions import ParamError, PlatCanNotDeleteError
from node_man.permissions import IsAdmin
from node_man.constants import ResponseCodeStatus, ProcType, PLUGIN_STATUS_DICT, \
    AUTO_STATUS_DICT

from common.log import logger
def get_proc_status1(request):
    resopnse = StreamingHttpResponse(stream_debugging())
    resopnse.__setitem__("Access-Control-Allow-Origin",'*')
    return resopnse

def get_proc_status(request):
    stream_debugging()
    resopnse = StreamingHttpResponse()
    resopnse.__setitem__("Access-Control-Allow-Origin",'*')
    return resopnse


def stream_debugging():


    logger.info(u"get_plugin_status_task:开始执行")
    hosts = Host.objects.filter(is_deleted=False)
    biz_list = hosts.values("bk_biz_id").distinct()

    bk_supplier_ids = {}
    for biz in biz_list:
        bk_supplier_ids[biz["bk_biz_id"]] = Business(bk_biz_id=biz["bk_biz_id"]).bk_supplier_id


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
        _key = "%s:%s:%s" % (host.inner_ip, bk_supplier_ids[host.bk_biz_id], host.bk_cloud_id)
        host_id_mapping[_key] = host
        if _hosts.has_key(bk_supplier_id):
            _hosts[bk_supplier_id].append(_host)
        else:
            _hosts[bk_supplier_id] = [_host]

    agent = GSEAgent()
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
                plugin_name = meta.get("name")
                version = row.get("version")

                _key = "%s:%s:%s" % (host.get("ip"), host.get("bk_supplier_id"), host.get("bk_cloud_id"))
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





