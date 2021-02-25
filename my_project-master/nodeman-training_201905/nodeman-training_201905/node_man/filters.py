# -*- coding: utf-8 -*-
"""
    数据过滤类
"""
import django_filters
from node_man.models import Host


class DemoFilter(django_filters.FilterSet):
    """
    https://django-filter.readthedocs.io/en/1.1.0/guide/usage.html
    https://django-filter.readthedocs.io/en/1.1.0/ref/filterset.html#fields
    可配置查询：
        a list of field names：['language', 'code']
        a dictionary of field names mapped to a list of lookups
        {
            'language': ['exact', 'contains'],
            'id': ['gt', 'lt'],
        }
        http://localhost:8000/snippets1.json?language=abap&id__gt=1
        # 支持外键：
        http://localhost:8000/snippets1.json?language__contains=python&owner__username=hongsong
    """

    @property
    def qs(self):
        parent = super(Host, self).qs
        return parent.filter(linenos=True)
        # return parent.filter(linenos=True) | parent.filter(id__gt=10)

    class Meta:
        model = Host
        # fields = ['language', 'code']
        fields = {
            'language': ['exact', 'contains'],
            'id': ['gt', 'lt'],
            'owner__username': ['exact'],
        }
