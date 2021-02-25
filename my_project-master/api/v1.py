# -*- coding:utf-8 -*-

from django.conf.urls import include, patterns, url

# 公共URL配置
urlpatterns = patterns(
    '',
    # 权限管理
    url(r'^sysmanage/', include('sysmanage.urls')),
    url(r'^change_task/', include('change_task.urls')),
    # 无module模块
    url(r'^misc/', include('misc.urls')),
    url(r'^', include('home_application.urls'))
)