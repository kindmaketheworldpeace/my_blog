# -*- coding: utf-8 -*-
from django.db.models import F
from change_task.serializers import ServicePrividerSerializer, RuleSerializer
from change_task.models import ServicePrivider, Rule
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from guardian.decorators import permission_required_or_403
from blueking.component.shortcuts import get_client_by_user
from component.drf.viewsets import ModelViewSet
from component.drf.serializer import CustomSerializer
from component.drf.generics import validate_fields
from component.drf.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class ServicePrividerViewSet(ModelViewSet):
    queryset = ServicePrivider.objects.all()
    serializer_class = ServicePrividerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = {'name': ['contains']}
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = CustomPageNumberPagination

    def create(self, request, *args, **kwargs):
        request.data['checkers'] = ",".join(request.data['checkers'])
        request.data['approvers'] = ",".join(request.data['approvers'])
        return super(ServicePrividerViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get("checkers"):
            request.data['checkers'] = ",".join(request.data['checkers'])
        if request.data.get("approvers"):
            request.data['approvers'] = ",".join(request.data['approvers'])
        return super(ServicePrividerViewSet, self).update(request, *args, **kwargs)


class RuleViewSet(ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    filter_fields = {'name': ['contains']}
    http_method_names = ['get', 'post', 'put', 'delete']
    pagination_class = CustomPageNumberPagination


