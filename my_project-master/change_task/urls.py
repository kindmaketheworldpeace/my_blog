# -*- coding: utf-8 -*-
from rest_framework import routers as drf_routers
from django.conf.urls import url
from change_task.views import (ServicePrividerViewSet, RuleViewSet)
from change_task.views.task import *
from change_task.views.scene import SceneViewSet

routers = drf_routers.DefaultRouter(trailing_slash=True)

routers.register(r'service_privider', ServicePrividerViewSet, base_name='user')

routers.register(r'rule', RuleViewSet, base_name='user')
# routers.register(r'scene_task', SceneTaskViewSet, base_name='task')
routers.register(r'scene', SceneViewSet, base_name='scene')
routers.register(r'scene_task', SceneTaskViewSet, base_name='scene_task')
routers.register(r'custom_task', CustomTaskViewSet, base_name='custom_task')


urlpatterns = [
     #url(r'^run_task/$', run_task),
]
urlpatterns += routers.urls
