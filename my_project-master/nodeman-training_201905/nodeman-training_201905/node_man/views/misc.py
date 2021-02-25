# -*- coding: utf-8 -*-
import re

from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.http import Http404, HttpResponseNotAllowed
from django.utils.translation import ugettext as _

from node_man.component.cmdb import Business
from node_man.models import Cloud, KV, Host
from node_man.component.viewsets import ModelViewSet
from node_man.serializers.misc import CloudSerializer, KvSerializer
from node_man.serializers.validators import gse_ip_validator, timeout_validator, url_validator
from node_man.component.exceptions import ParamError, PlatCanNotDeleteError
from node_man.permissions import IsAdmin
from node_man.constants import ResponseCodeStatus


class CloudViewSet(ModelViewSet):
    queryset = Cloud.objects.all()
    serializer_class = CloudSerializer
    pagination_class = None

    def get_queryset(self):
        """
        查询业务对应开发商下的云区域列表
        """
        bk_biz_id = self.kwargs.get('bk_biz_id')
        queryset = Cloud.objects.all().filter(is_deleted=False, bk_biz_id=bk_biz_id)
        bk_supplier_id = Business(bk_biz_id).bk_supplier_id

        if bk_supplier_id is not None:
            queryset = queryset.filter(bk_supplier_id=bk_supplier_id)
        return queryset

    def perform_create(self, serializer):
        """
        云区域写入cmdb
        """
        bk_cloud_id = Business.get_or_create_plat_id(self.request.data.get('bk_cloud_name'))
        try:
            cloud_obj = self.queryset.get(bk_cloud_id=bk_cloud_id, bk_biz_id=self.kwargs.get('bk_biz_id'))
        except Cloud.DoesNotExist as exc:
            try:
                cloud_obj = self.queryset.get(bk_cloud_id=bk_cloud_id, bk_biz_id='-1')
            except Cloud.DoesNotExist as exc:
                cloud_obj = None
        serializer.instance = cloud_obj
        serializer.save(
            bk_biz_id=self.kwargs.get('bk_biz_id'),
            bk_cloud_id=bk_cloud_id,
            bk_supplier_id=Business(bk_biz_id=self.kwargs.get('bk_biz_id')).bk_supplier_id,
            creator=self.request.user.username,
        )

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['related_biz_id'] = self.kwargs.get('bk_biz_id')
        return serializer_class(*args, **kwargs)

    def perform_destroy(self, instance):
        '''
        删除一个云区域
        '''
        if Host.objects.filter(bk_cloud_id=instance.bk_cloud_id, is_deleted=False).count() > 0:
            hosts = Host.objects.filter(bk_cloud_id=instance.bk_cloud_id, is_deleted=False).values_list("inner_ip",
                                                                                                        flat=True)
            errors = _(u'该云区域在其他业务下存在机器：%s') % ",".join(hosts)
            raise PlatCanNotDeleteError(errors)
        result = Business.delete_plat(instance.bk_cloud_id)
        if result == 'success':
            instance.destroy()
        return Response()

    @detail_route(methods=['post'], url_path='disvisible')
    def disvisible(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.disvisible()
        return Response()

    @detail_route(methods=['post'], url_path='envisible')
    def envisible(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.envisible()
        return Response()

    @detail_route(methods=['post'], url_path='rename')
    def rename(self, request, *args, **kwargs):
        # result = Business.rename_plat(instance.bk_cloud_id)
        instance = self.get_object()
        if not request.data.get("bk_cloud_name"):
            raise ParamError(_(u"修改的名称不能为空"))
        Business.rename_plat(instance.bk_cloud_id, request.data.get("bk_cloud_name"))
        instance.rename(request.data.get("bk_cloud_name"))
        return Response()


class GatewayCloudViewSet(CloudViewSet):
    '''
    用于网关接口 取消权限验证
    '''
    permission_class = ()

    def perform_create(self, serializer):
        """
        云区域写入cmdb
        """
        bk_cloud_id = Business.get_or_create_plat_id(self.request.data.get('bk_cloud_name'))
        try:
            cloud_obj = self.queryset.get(bk_cloud_id=bk_cloud_id, bk_biz_id=self.kwargs.get('bk_biz_id'))
        except Cloud.DoesNotExist as exc:
            try:
                cloud_obj = self.queryset.get(bk_cloud_id=bk_cloud_id, bk_biz_id='-1')
            except Cloud.DoesNotExist as exc:
                cloud_obj = None
        serializer.instance = cloud_obj
        serializer.save(
            bk_biz_id=self.kwargs.get('bk_biz_id'),
            bk_cloud_id=bk_cloud_id,
            bk_supplier_id=Business(bk_biz_id=self.kwargs.get('bk_biz_id')).bk_supplier_id,
            creator=self.request.user.username,
            is_visible=False
        )


class KvViewSet(ModelViewSet):
    SPECIAL_VALIDATORS = {
        'nginx': url_validator,
        'timeout': timeout_validator,
        'gse': gse_ip_validator,
    }
    queryset = KV.objects.all()
    serializer_class = KvSerializer
    pagination_class = None
    permission_classes = (IsAdmin,)

    def get_object_response(self, key):
        """获取key对应的值"""
        try:
            value = self.queryset.get(key=key)
            return Response({
                "data": value.v_json,
                "code": ResponseCodeStatus.OK,
                "result": True,
                "message": 'success'
            })
        except KV.DoesNotExist:
            raise Http404(_(u'配置信息不存在，请先配置'))

    def set_object_response(self, key, data):
        """更新key对应的值"""
        try:
            instance = self.queryset.get(key=key)
        except KV.DoesNotExist:
            instance = None

        serializer = self.get_serializer(
            instance=instance,
            data=data,
            validators=[self.SPECIAL_VALIDATORS.get(key)]
        )

        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response()

    @list_route(methods=['get', 'post'], url_path='kv')
    def kv(self, request, *args, **kwargs):

        if request.method == 'GET':
            key = self.request.query_params.get('key')
            return self.get_object_response(key)

        if request.method == 'POST':
            key = self.request.data.get('key')
            return self.set_object_response(key, request.data)

        raise HttpResponseNotAllowed(_(u'方法%s不被允许') % request.method)
