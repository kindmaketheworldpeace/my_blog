# -*- coding: utf-8 -*-
from django.conf.urls import url

from misc import views

urlpatterns = [
    url(r'^get_host_by_module/$', views.get_host_by_module),
    url(r'^get_host/$', views.get_host),
    url(r'^get_bk_user/$', views.get_bk_user),
]
