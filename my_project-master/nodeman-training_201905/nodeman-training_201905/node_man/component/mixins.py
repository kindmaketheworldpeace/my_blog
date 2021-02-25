# -*- coding: utf-8 -*-
"""
    公共混用类，拷贝自paas-ci项目
"""
from rest_framework.response import Response
from rest_framework import status

from node_man.constants import ResponseCodeStatus
from node_man.permissions import IsBizOwner, NginxSettingCheck


class ApiGenericMixin(object):
    """API视图类通用函数"""
    # TODO 权限部分加载基类中
    permission_classes = (NginxSettingCheck, IsBizOwner)

    def finalize_response(self, request, response, *args, **kwargs):
        """统一数据返回格式"""
        if response.data is None:
            response.data = {
                'result': True,
                'code': ResponseCodeStatus.OK,
                'message': 'success',
                'data': None
            }
        elif isinstance(response.data, (list, tuple)):
            response.data = {
                'result': True,
                "code": ResponseCodeStatus.OK,
                "message": 'success',
                "data": response.data,
            }
        elif isinstance(response.data, dict) and "code" not in response.data:
            response.data = {
                'result': True,
                "code": ResponseCodeStatus.OK,
                "message": 'success',
                "data": response.data,
            }
        if response.status_code == status.HTTP_204_NO_CONTENT and request.method == "DELETE":
            response.status_code = status.HTTP_200_OK
            # response.status_text = "OK"

        if response.status_code == status.HTTP_201_CREATED and request.method == "POST":
            response.status_code = status.HTTP_200_OK


        return super(ApiGenericMixin, self).finalize_response(
            request, response, *args, **kwargs
        )

    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        request = super(ApiGenericMixin, self).initialize_request(request, *args, **kwargs)
        if request.method == "POST" and not request.META.get("HTTP_X_CSRFTOKEN"):
            request.META["HTTP_X_CSRFTOKEN"] = request.data.get("csrfmiddlewaretoken", "")
        return request


class ApiListModelMixin(object):
    """
    List a queryset.
    """

    def list(self, request, bk_biz_id, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
