# -*- coding: utf-8 -*-
from component.drf.viewsets import BaseModelViewSet
from change_task.models import Scene
from change_task.serializers.serializers import SceneSerializer
from component.drf.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from component.drf.permissions import (IsAdmin, )


class SceneViewSet(BaseModelViewSet):
    queryset = Scene.objects.all().order_by('-updated_by')
    serializer_class = SceneSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAdmin, )
    # 使用过滤器
    filter_backends = (DjangoFilterBackend,)
    # 定义需要使用过滤器的字段
    filter_fields = {
        'name': ['exact', 'contains', 'startswith'],
        'creator': ['exact', 'contains', 'startswith'],
    }
    http_method_names = ['get', 'post', 'put', 'delete']

    # 私有场景仅创建人可见，公共场景所有人可见
    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(Q(display_role__contains=user) | Q(display_type='OPEN'))
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create and return a new `Scene` instance, given the validated data.
        """
        return super(SceneViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update and return an existing `Scene` instance, given the validated data.
        """
        return super(SceneViewSet, self).update(request, *args, **kwargs)