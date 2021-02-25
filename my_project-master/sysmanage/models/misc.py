# -*- coding: utf-8 -*-
"""
杂种models文件
"""
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sysmanage.models.basic import Model
from sysmanage.managers import Manager


class Setting(Model):
    type_choices = (
        ("int", "int"),
        ("str", "str"),
        ("json", "json")
    )
    name = models.CharField(_(u'名称'), max_length=50, unique=True)
    description = models.CharField(_(u'描述信息'), max_length=254, blank=True)
    value = models.TextField(_(u'值'), blank=True)
    type = models.CharField(_(u'值类型'), max_length=20, choices=type_choices, default="str")
    is_show = models.BooleanField(_(u'是否显示'), default=True)

    objects = Manager()

    class Meta:
        verbose_name = _(u'设置')
        verbose_name_plural = _(u'设置')

    def __unicode__(self):
        return self.name

    def get_value(self):
        """获取设置项值"""
        value = self.value
        if self.type == 'int':
            value = int(self.value)
        elif self.type == 'json':
            try:
                value = json.loads(self.value)
            except:
                pass
        return value


class Log(models.Model):
    operator = models.CharField(_(u'操作者'), max_length=50)
    operated_object = models.CharField(_(u'操作对象'), max_length=50, blank=True)
    operated_type = models.CharField(_(u'操作类型'), max_length=50, blank=True)
    operator_date = models.DateTimeField(_(u'操作时间'), null=True, blank=True)
    content = models.TextField(_(u'操作内容'), blank=True)
    ip_addr = models.CharField(_(u'IP地址'), max_length=50, null=True, blank=True)
    is_success = models.BooleanField(_(u'是否成功'), default=True)

    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Log')
        ordering = ["-id"]

    def __unicode__(self):
        return self.operator_date.strftime("%Y-%m-%d %H:%M:%S")
