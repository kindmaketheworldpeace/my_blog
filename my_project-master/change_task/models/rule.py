# -*- coding: utf-8 -*-

import jsonfield
from django.db import models

from change_task.models.basic import Model
from change_task.managers import Manager
from component.constants import (
    LEN_SHORT,
    LEN_NORMAL,
    LEN_X_LONG,
    EMPTY_LIST,
    ROLE_CHOICES,
)

class ServicePrivider(Model):
    name = models.CharField(u"服务商名称", max_length=LEN_NORMAL)
    description = models.TextField(u"描述信息", blank=True)
    # 前后通过逗号隔开，ex: ,kris,
    checkers = models.CharField(u"复核者", max_length=LEN_X_LONG, blank=True)
    checkers_type = models.CharField(u"复核者类型", max_length=LEN_SHORT, choices=ROLE_CHOICES, default="PERSON")
    # 前后通过逗号隔开，ex: ,admin,
    approvers = models.CharField(u"审批者", max_length=LEN_X_LONG, blank=True)
    approvers_type = models.CharField(u"审批者类型", max_length=LEN_SHORT, choices=ROLE_CHOICES, default="PERSON")
    rule_priority_list = jsonfield.JSONField(u"规则优先级排序", default=EMPTY_LIST)

    objects = Manager()

    class Meta:
        verbose_name = u"服务商"
        verbose_name_plural = u"服务商"

    def __unicode__(self):
        return "%s" % self.name


class Rule(Model):
    RESULT_CHOICES = [
        ("REJECT", u"拒绝"),
        ("CHECK", u"复核"),
        ("PASS", u"通过"),
    ]

    name = models.CharField(u"规则名称", max_length=LEN_NORMAL)
    description = models.TextField(u"描述信息", blank=True)
    is_enable = models.BooleanField(u"是否启用", default=True)
    """
    {
        "expressions": [
            {
                "expressions": [
                    {
                        "key": "time",
                        "condition": "in",
                        "value": ["9:00", "21:00"]
                    }
                ],
                "type": "and"
            }
        ],
        "type": "and"
    }
    说明：
    [key] date（日期，对应：工作日、不限）time（时间）biz（业务）ip（IP地址）ip_percent_biz（主机占业务百分比）
    [condition] ==（等于）!=（不等于）>（大于）>=（大于等于）<（小于）<=（小于等于）in（属于）not in（不属于）exclusive（互斥）
    """
    condition = jsonfield.JSONField(u"规则条件", default=EMPTY_LIST)
    result = models.CharField(u"规则结果", max_length=LEN_SHORT, choices=RESULT_CHOICES)
    service_privider = models.ForeignKey(ServicePrivider, help_text=u"服务商", related_name="rules")

    objects = Manager()

    class Meta:
        verbose_name = u"规则"
        verbose_name_plural = u"规则"

    def __unicode__(self):
        return "%s(%s)" % (self.name, self.service_privider.name)