# -*- coding: utf-8 -*-
"""
    配置平台查询接口
"""
from rest_framework import serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from node_man.component.cmdb import Business
from node_man.component.viewsets import GenericViewSet
from node_man.utils.basic import safe_cast


class CmdbViewSet(GenericViewSet):
    """
    配置平台相关接口
    """
    serializer_class = serializers.Serializer
    lookup_value_regex = '\d+'
    lookup_field = 'bk_biz_id'

    @list_route(methods=['get'], url_path='applications')
    def applications(self, request):
        """查询用户有权限的业务列表"""
        _arr = Business.get_app_by_user(request.user)
        return Response(_arr)

    @detail_route(methods=['get'], url_path='topo')
    def topo(self, request, bk_biz_id=None):
        """查询业务下的大区和模块列表信息"""
        add_hosts = safe_cast(request.query_params.get('add_hosts'), int, 0)
        return Response(Business(bk_biz_id=bk_biz_id).get_set_module_tree(add_hosts))

    @detail_route(methods=['get'], url_path='get_app_host_list')
    def get_app_host_list(self, request, bk_biz_id=None):
        """查询业务下主机列表信息"""
        return Response(Business(bk_biz_id=bk_biz_id).get_app_host_list())

    @list_route(methods=['get'], url_path='plats')
    def get_all_plat(self, request):
        """查询所有云区域信息"""
        return Response(Business.get_all_plat())
