# -*- coding: utf-8 -*-
"""
用于本地开发环境的全局配置
"""

# 多人开发时，无法共享的本地配置可以放到新建的 local_settings.py 文件中
# 并且把 local_settings 加入版本管理忽略文件中
try:
    from local_settings import *  # noqa
except ImportError:
    pass
