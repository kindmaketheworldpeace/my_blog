# -*- coding: utf-8 -*-

from django.test import TestCase

import settings_unittest as test_settings


class BaseTest(TestCase):
    """测试类"""

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        if hasattr(test_settings, name):
            return getattr(test_settings, name)
        else:
            return ""
