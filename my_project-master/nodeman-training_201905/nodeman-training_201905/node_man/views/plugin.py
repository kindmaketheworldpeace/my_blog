# -*- coding: utf-8 -*-
"""
    配置平台查询接口
"""

from rest_framework.decorators import list_route
from rest_framework.response import Response

from node_man.component.viewsets import GenericViewSet
from node_man.constants import ResponseCodeStatus
from node_man.serializers.misc import (
    PluginSerializer, GsePluginSerializer,
    ProcessControlInfoSerializer,
    ProcessPackageSerializer)
from rest_framework.exceptions import ValidationError

# TODO: 临时处理代码 校验错误返回改为字符型
# 最终解决方案是修改公共处理函数 将返回字段及类型统一

def get_ex_msg(e):
    messages = []
    detail = e.detail
    if isinstance(e.detail, dict):
        messages = []
        detail = e.detail
        for k, v in detail.iteritems():
            if isinstance(v, list):
                messages.append("%s: %s" % (k, ",".join(v)))
            else:
                messages.append("%s: %s" % (k, v))
    elif isinstance(e.detail, list):
        for v in detail:
            messages.append(v)
    elif isinstance(detail, basestring):
        messages.append(detail)
    else:
        return detail
    return ";".join(messages)

class PluginViewSet(GenericViewSet):
    '''
    获取agent运行状态和版本信息
    '''
    serializer_class = PluginSerializer

    @list_route(methods=["post"], url_path="add")
    def add(self, request, *args, **kwargs):
        data = request.data

        gseplugindesc = data.get("gseplugindesc")
        packages = data.get("packages")
        proccontrol = data.get("proccontrol")
        try:
            process_serializer = GsePluginSerializer(data=gseplugindesc)
            process_serializer.is_valid(raise_exception=True)
            process_serializer.save()

            package_serializer = ProcessPackageSerializer(data=packages)
            package_serializer.is_valid(raise_exception=True)
            package_serializer.save()

            process_info_serializer = ProcessControlInfoSerializer(
                data=proccontrol)
            process_info_serializer.is_valid(raise_exception=True)
            process_info_serializer.save()
        except ValidationError as ve:
            return Response({
                "result": False,
                "data": None,
                "code": ResponseCodeStatus.VALIDATE_ERROR,
                "message": get_ex_msg(ve),
            })
        except:
            raise

        return Response({
            "result": True,
            "data": {
                "process": process_serializer.data,
                "package": package_serializer.data,
                "process_info": process_info_serializer.data,
            },
            "code": ResponseCodeStatus.OK,
            "message": "success"
        })
