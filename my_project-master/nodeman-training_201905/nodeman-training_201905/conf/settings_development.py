# -*- coding: utf-8 -*-
"""
用于本地开发环境的全局配置
"""
from settings import APP_ID
from settings import MIDDLEWARE_CLASSES

# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': APP_ID
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
    #     'NAME': APP_ID,  # 数据库名 (默认与APP_ID相同)
    #     'USER': 'root',  # 你的数据库user
    #     'PASSWORD': 'root',  # 你的数据库password
    #     'HOST': '127.0.0.1',  # 开发的时候，使用localhost
    #     'PORT': '3306',  # 默认3306
    # },
}
# ==============================================================================
# Middleware and apps
# ==============================================================================
# # CELERY_ALWAYS_EAGER = True
MIDDLEWARE_CLASSES = (
                         'corsheaders.middleware.CorsMiddleware',
                         'account.middlewares.DisableCSRFCheck',  # 本地不需要校验CSRF
                     ) + MIDDLEWARE_CLASSES

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings 加入版本管理忽略文件中
try:
    from local_settings import *  # noqa
except ImportError:
    pass
