# -*- coding: utf-8 -*-
"""
    配置平台查询接口
"""

import json
import datetime
import traceback

from django.http import Http404
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response

from node_man.component.exceptions import NginxSettingError, \
    InitializeError
from node_man.component.viewsets import GenericViewSet
from node_man.constants import ResponseCodeStatus
from node_man.models import KV
from node_man.serializers.misc import (
    GsePluginSerializer,
    ProcessControlInfoSerializer,
    ProcessPackageSerializer)
from node_man.utils.basic import read_remote_file_content
from common.log import logger


class GlobalOperateViewSet(GenericViewSet):
    '''
    获取agent运行状态和版本信息
    '''
    http_method_names = ["post", "get"]
    queryset = KV.objects.all()
    serializer_class = serializers.Serializer

    @list_route(methods=["post", "get"], url_path="init")
    def init(self, request, *args, **kwargs):
        try:
            value = self.queryset.get(key='nginx')
            nginx_server = value.v_json
        except KV.DoesNotExist:
            raise NginxSettingError(_(u'nginx配置信息为空'))

        # 插入初始化信息
        KV.objects.update_or_create(
            defaults={
                'v_json': {
                    'user': request.user.username,
                    'time': str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                }
            },
            key='plugin_config',
        )

        data = []
        inner_url = self._fetch_inner_url(nginx_server)
        try:
            init_nodeman_json = read_remote_file_content(inner_url)
        except (ValueError, Http404) as err:
            raise InitializeError(_(str(err)))
        except Exception as err:
            raise InitializeError(_(u"未知错误:%s" % err))

        for i,row in enumerate(init_nodeman_json):
            try:
                result = self._init(row)
            except Exception as err:
                logger.error("init_nodeman_json data incorrect: {}".format(str(err)))
                logger.error("incorrect data: {}, index: {}".format(init_nodeman_json, i))
                logger.error(traceback.format_exc())
            data.append(result)

        return Response({
            "result": True,
            "data": data,
            "code": ResponseCodeStatus.OK,
            "message": "success"
        })

    def _fetch_inner_url(self, data):
        return "{}/init_nodeman.json".format(data.get("inner_url", ""))

    def _init(self, data):
        gseplugindesc = data.get("gseplugindesc")
        packages = data.get("packages")
        proccontrol = data.get("proccontrol")

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

        return {
            "gseplugindesc": process_serializer.data,
            "packages": package_serializer.data,
            "proccontrol": process_info_serializer.data,
        }
