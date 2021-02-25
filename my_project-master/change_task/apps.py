# -*- coding: utf-8 -*-

"""
初始化内置APP数据
"""

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def app_ready_handler(sender, **kwargs):
    pass


class ChangeTaskConfig(AppConfig):
    name = "change_task"

    def ready(self):
        post_migrate.connect(app_ready_handler, sender=self)
