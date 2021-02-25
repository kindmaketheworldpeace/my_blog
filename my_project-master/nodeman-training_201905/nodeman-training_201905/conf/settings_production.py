# -*- coding: utf-8 -*-
"""
用于正式环境的全局配置
"""
import os

from settings import APP_ID

# ===============================================================================
# 数据库设置, 正式环境数据库设置
# ===============================================================================
DB_USERNAME = os.environ.get('BKAPP_DB_USERNAME', '')
DB_PASSWORD = os.environ.get('BKAPP_DB_PASSWORD', '')
DB_HOST = os.environ.get('BKAPP_DB_HOST', '')
DB_PORT = os.environ.get('BKAPP_DB_PORT', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
        'NAME': APP_ID,  # 数据库名 (默认与APP_ID相同)
        'USER': os.environ.get('DB_USERNAME', DB_USERNAME),
        'PASSWORD': os.environ.get('DB_PASSWORD', DB_PASSWORD),
        'HOST': os.environ.get('DB_HOST', DB_HOST),
        'PORT': os.environ.get('DB_PORT', DB_PORT),
    }
}
