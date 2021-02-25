# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from rest_framework.decorators import detail_route, list_route
from django_filters.rest_framework import DjangoFilterBackend
from component.drf.viewsets import TaskModelViewSet
from change_task.serializers.task_serializer import (SceneTaskSerializer, CustomTaskSerializer)
from change_task.models import (SceneTask, CustomTask)
from component.drf.pagination import CustomPageNumberPagination
from component.drf.permissions import (IsOwnerOrReadOnly, )
from component.drf.generics import validate_fields


class SceneTaskViewSet(TaskModelViewSet):
    queryset = SceneTask.objects.all().order_by('-updated_by')
    serializer_class = SceneTaskSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsOwnerOrReadOnly, )
    # 使用过滤器
    filter_backends = (DjangoFilterBackend, )
    # 定义需要使用过滤器的字段
    filter_fields = {
        'name': ['exact', 'contains', 'startswith'],
        'creator': ['exact', 'contains', 'startswith'],
    }
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        """
        Create and return a new `SceneTask` instance, given the validated data.
        """

        return super(SceneTaskViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update and return an existing `SceneTask` instance, given the validated data.
        """
        return super(SceneTaskViewSet, self).update(request, *args, **kwargs)


class CustomTaskViewSet(TaskModelViewSet):
    queryset = CustomTask.objects.all().order_by('-updated_by')
    serializer_class = CustomTaskSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsOwnerOrReadOnly, )
    # 使用过滤器
    filter_backends = (DjangoFilterBackend, )
    # 定义需要使用过滤器的字段
    filter_fields = {
        'name': ['exact', 'contains', 'startswith'],
        'creator': ['exact', 'contains', 'startswith'],
    }

    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        """
        Create and return a new `CustomTask` instance, given the validated data.
        """

        return super(CustomTaskViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update and return an existing `CustomTask` instance, given the validated data.
        """
        return super(CustomTaskViewSet, self).update(request, *args, **kwargs)
