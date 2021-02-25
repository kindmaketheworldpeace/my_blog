# -*- coding: utf-8 -*-

"""
表级别操作
"""

from django.db import models
from django.db.models import QuerySet


class SoftDeletQuerySet(QuerySet):
    """支持软删除"""

    def delete(self):
        return super(SoftDeletQuerySet, self).update(is_deleted=True)

    def hard_delete(self):
        return super(SoftDeletQuerySet, self).delete()


class Manager(models.Manager):
    """支持软删除"""

    def get_queryset(self):
        return SoftDeletQuerySet(self.model).filter(is_deleted=False)
