# <<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
用于本地开发环境的全局配置
"""
import os
from settings import APP_ID


# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
# '''
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',      # 默认用mysql
#         'NAME': 'change-console',              # 数据库名 (默认与APP_ID相同)
#         'USER': "root",     # 你的数据库user
#         'PASSWORD': "111111",  # 你的数据库password
#         'HOST': "127.0.0.1",         # 数据库HOST
#         'PORT': 3306,         # 默认3306
#     },
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认用mysql
        'NAME': 'change-console',                        # 数据库名 (默认与APP_ID相同)
        'USER': 'root',                        # 你的数据库user
        'PASSWORD': '111111',                        # 你的数据库password
        'HOST': '127.0.0.1',                   # 开发的时候，使用localhost
        'PORT': '3306',                        # 默认3306
    },
}
# 将celery异步任务更改为同步
CELERY_ALWAYS_EAGER = True
# =======
# -*- coding: utf-8 -*-
"""
用于本地开发环境的全局配置
"""
import os
from settings import APP_ID


# ===============================================================================
# 数据库设置, 本地开发数据库设置
# ===============================================================================
# '''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',      # 默认用mysql
        'NAME': APP_ID,                            # 数据库名 (默认与APP_ID相同)
        'USER': "root",     # 你的数据库user
        'PASSWORD': "passwd", # 你的数据库password
        'HOST': "127.0.0.1",         # 数据库HOST
        'PORT': 3306,         # 默认3306
    },
}

# 将celery异步任务更改为同步
CELERY_ALWAYS_EAGER = True
# >>>>>>> e78c6b0e89f2b39b931107e43eb0e2113cdd0910
