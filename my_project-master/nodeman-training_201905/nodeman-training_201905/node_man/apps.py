# -*- coding: utf-8 -*-
"""
执行app初始化操作，步骤位于migrate操作后，需要print信息到标准输出
http://www.koopman.me/2015/01/django-signals-example/
"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate

from common.log import logger


def app_ready_handler(sender, **kwargs):
    print 'app_ready_handler'
    try:
        pass
    except Exception as e:
        logger.error(e)


class NodeManConfig(AppConfig):
    name = 'node_man'

    def ready(self):
        post_migrate.connect(app_ready_handler, sender=self)
