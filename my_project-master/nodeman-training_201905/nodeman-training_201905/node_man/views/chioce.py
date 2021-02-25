# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response

from node_man.component.viewsets import GenericViewSet
from node_man.constants import (
    OS_CHOICES, ResponseCodeStatus, FUNCTION_LIST, CATEGORY_LIST,
    JOB_TYPE_DICT, JobType, JOB_TUPLE)


class ChoiceViewSet(GenericViewSet):
    serializer_class = serializers.Serializer

    @list_route(methods=['get'], url_path='os_type')
    def os_type(self, request):
        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": [dict(id=k, name=v) for k, v in OS_CHOICES]
        })

    @list_route(methods=['get'], url_path='op')
    def op(self, request):
        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": FUNCTION_LIST
        })

    @list_route(methods=['get'], url_path='category')
    def category(self, request):
        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": CATEGORY_LIST
        })

    @list_route(methods=['get'], url_path='job_type')
    def job_type(self, request):
        data = []
        for k in JOB_TUPLE:

            # if k in [JobType.UPDATE_AUTHINFO, JobType.IMPORT_PROXY, JobType.IMPORT_AGENT, JobType.IMPORT_PAGENT]:
            #     continue

            _k = k.split("_")
            obj = _k[1]
            v = JOB_TYPE_DICT.get(k) + obj
            row = {
                "id": k,
                "name": v
            }
            data.append(row)
        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": data
        })
