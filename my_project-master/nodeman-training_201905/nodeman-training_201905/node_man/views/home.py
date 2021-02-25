# -*- coding: utf-8 -*-
"""
    模板相关视图
    相关页面：
        首页
"""
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet as _ViewSet
from django.utils.translation import ugettext as _

from common.mymako import render_mako_context
from node_man import settings


def index(request):
    # from node_man.backend.scheduler import clean_expired_info
    # clean_expired_info()
    title = _(u"节点管理")
    return render_mako_context(request, "index.html", {"title": title})


class HomeViewSet(_ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = settings.INDEX_TEMPLATE

    def index(self, request, *args, **kwargs):
        return Response({'username': 'pitou'})
