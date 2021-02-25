# -*- coding: utf-8 -*-
import sys
from django.test import TestCase
from node_man.models import Plat


class TestHelloWorld(TestCase):
    # python manage.py dumpdata --indent 2 app -o fixtures/app.json --format json
    fixtures = ['app.json']

    def setUp(self):
        print sys._getframe().f_code.co_name
        Plat.objects.create(plat_id="hello", operator="world", company_id="123", name="test", biz_id="111")

    def tearDown(self):
        print sys._getframe().f_code.co_name

    def test_secure_info(self):
        print sys._getframe().f_code.co_name
        sec = Plat.objects.get(plat_id="hello")
        self.assertEqual(sec.operator, "world")

# https://realpython.com/blog/python/test-driven-development-of-a-django-restful-api/
# python manage.py test --settings=test_project.settings_test app

# 536  python manage.py test                                            自动查找test_文件
# 536  python manage.py test -v 3                                       打印详情
# 538  python manage.py test tests.tests_3_hello_world_                 指定文件
# 539  python manage.py test -k tests.tests_3_hello_world_              保留测试数据库
# 545  python manage.py test tests.tests_3_hello_world_.TestHelloWorld  指定模块
# 557  python manage.py test tests -p *hello_world_*                    指定目录和文件匹配规则

# 查找test_*.py，查找文件中继承了TestCase的类，查找test_函数

# When using SQLite, the tests will use an in-memory database by default
#  (i.e., the database will be created in memory, bypassing the filesystem entirely!).
# 使用sqlite3可加快测试
