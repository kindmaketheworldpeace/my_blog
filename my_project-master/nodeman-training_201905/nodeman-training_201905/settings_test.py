# -*- coding: utf-8 -*-
"""
    提升测试速度：使用内存型数据库sqlite
"""
from settings import *

# ===============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': APP_ID
    }
}

# 开启同步模式，方便本地调试
# CELERY_ALWAYS_EAGER = True
