# -*- coding: utf-8 -*-
from django.db import models

from component.constants import (
    LEN_NORMAL,
)


class Model(models.Model):
    """基础字段"""

    FIELDS = ('creator', 'create_at', 'updated_by', 'update_at', 'end_at')

    creator = models.CharField(u"创建人", max_length=LEN_NORMAL, null=True, blank=True)
    create_at = models.DateTimeField(u"创建时间", auto_now_add=True)
    update_at = models.DateTimeField(u"更新时间", auto_now=True)
    updated_by = models.CharField(u"修改人", max_length=LEN_NORMAL, null=True, blank=True)
    end_at = models.DateTimeField(u"结束时间", null=True, blank=True)
    is_deleted = models.BooleanField(u"是否软删除", default=False, db_index=True)

    _objects = models.Manager()
    objects = models.Manager()

    class Meta:
        app_label = "sysmanage"
        abstract = True

    def delete(self, using=None):
        self.is_deleted = True
        self.save()

    def hard_delete(self, using=None):
        super(Model, self).delete()
