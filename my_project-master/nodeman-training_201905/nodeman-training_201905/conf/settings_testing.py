# -*- coding: utf-8 -*-
"""
用于测试环境的全局配置
"""
import os

from settings import APP_ID
from settings import MIDDLEWARE_CLASSES

# ===============================================================================
# 数据库设置, 测试环境数据库设置
# ===============================================================================
DB_NAME = os.environ.get('BKAPP_APP_ID', APP_ID)
DB_USERNAME = os.environ.get('BKAPP_DB_USERNAME', '')
DB_PASSWORD = os.environ.get('BKAPP_DB_PASSWORD', '')
DB_HOST = os.environ.get('BKAPP_DB_HOST', '')
DB_PORT = os.environ.get('BKAPP_DB_PORT', '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
        'NAME': DB_NAME,  # 数据库名 (默认与APP_ID相同)
        'USER': os.environ.get('DB_USERNAME', DB_USERNAME),
        'PASSWORD': os.environ.get('DB_PASSWORD', DB_PASSWORD),
        'HOST': os.environ.get('DB_HOST', DB_HOST),
        'PORT': os.environ.get('DB_PORT', DB_PORT),
    }
}

# ==============================================================================
# Middleware and apps
# ==============================================================================
MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'account.middlewares.DisableCSRFCheck',
) + MIDDLEWARE_CLASSES
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
