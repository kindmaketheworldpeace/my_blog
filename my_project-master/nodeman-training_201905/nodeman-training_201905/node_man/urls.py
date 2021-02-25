# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers as drf_routers

from views import (
    index, CloudViewSet, JobViewSet,
    CmdbViewSet, KvViewSet,
    HostViewSet, HostStatusViewSet,
    HostLogViewSet, TestViewSet, GsePluginViewSet,
    ProcessPackageViewSet, ProcessControlInfoViewSet,
    ChoiceViewSet, JobLogViewSet, GatewayJobViewSet,
    GatewayHostStatusViewSet, PluginViewSet, GlobalOperateViewSet, GatewayCloudViewSet)

routers = drf_routers.DefaultRouter(trailing_slash=True)
gw_routers = drf_routers.DefaultRouter(trailing_slash=True)

# 注册各模块接口
routers.register(r'cmdb', CmdbViewSet, base_name='cmdb')
routers.register(r'config', KvViewSet, base_name='config')
routers.register(r'tests', TestViewSet, base_name='tests')
routers.register(r'choice', ChoiceViewSet, base_name='choice')
routers.register(r'global_operate', GlobalOperateViewSet, base_name='global_operate')

# 插件/进程相关信息
routers.register(r'process', GsePluginViewSet)
routers.register(r'(?P<category>\w+)/process', GsePluginViewSet)
routers.register(r'package', ProcessPackageViewSet)
routers.register(r'(?P<process>\w+)/package', ProcessPackageViewSet)
routers.register(r'process_info', ProcessControlInfoViewSet)

# 任务日志
routers.register(r'logs/(?P<job_id>\d+)', JobLogViewSet)

# 路径固定添加bk_biz_id，方便业务界别权限校验
routers.register(r'(?P<bk_biz_id>\d+)/clouds', CloudViewSet)
routers.register(r'(?P<bk_biz_id>\d+)/tasks', JobViewSet)
routers.register(r'(?P<bk_biz_id>\d+)/hosts', HostViewSet)
routers.register(r'(?P<bk_biz_id>\d+)/logs', HostLogViewSet)
routers.register(r'(?P<bk_biz_id>\d+)/host_status', HostStatusViewSet)

# 网关用
gw_routers.register(r'process', GsePluginViewSet)
gw_routers.register(r'(?P<category>\w+)/process', GsePluginViewSet)
gw_routers.register(r'package', ProcessPackageViewSet)
gw_routers.register(r'(?P<process>\w+)/package', ProcessPackageViewSet)
gw_routers.register(r'process_info', ProcessControlInfoViewSet)
gw_routers.register(r'(?P<bk_biz_id>\d+)/clouds', GatewayCloudViewSet)

gw_routers.register(r'(?P<bk_biz_id>\d+)/tasks', GatewayJobViewSet)
gw_routers.register(r'(?P<bk_biz_id>\d+)/host_status', GatewayHostStatusViewSet)
gw_routers.register(r'(?P<bk_biz_id>\d+)/logs', HostLogViewSet)

# 仅用于后台更新插件 接口不暴露给外部查看
gw_routers.register(r'plugin', PluginViewSet, base_name='plugin')

urlpatterns = [
    url(r'^$', index),
    url(r'api/', include(routers.urls)),
    url(r'gateway/', include(gw_routers.urls)),
]
