# -*- coding: utf-8 -*-

from rest_framework import viewsets
from component.drf.mixins import ApiGenericMixin
from change_task.models import ServicePrivider
from django.db.models import Q


class ModelViewSet(ApiGenericMixin, viewsets.ModelViewSet):
    pass


# 基础字段自动填充
class BaseModelViewSet(ApiGenericMixin, viewsets.ModelViewSet):

    def perform_create(self, serializer):
        base_dict = {
            "creator": self.request.user,
            "updated_by": self.request.user
        }
        serializer.save(**base_dict)

    def perform_update(self, serializer):
        base_dict = {
            "updated_by": self.request.user
        }
        serializer.save(**base_dict)


# 任务对象视图，任务仅创建者和审核者可见
class TaskModelViewSet(BaseModelViewSet):

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return self.queryset
        service_providers = ServicePrivider.objects.filter(Q(checkers__contains=user) | Q(approvers__contains=user))
        if service_providers:
            sp_names = service_providers.values('name')
            queryset = self.queryset.filter(Q(creator=user) | Q(serivce_privider__in=sp_names))
        else:
            queryset = self.queryset.filter(creator=user)
        return queryset


class ViewSet(ApiGenericMixin, viewsets.ViewSet):
    pass


class GenericViewSet(ApiGenericMixin, viewsets.GenericViewSet):
    pass
