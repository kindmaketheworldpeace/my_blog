# -*- coding: utf-8 -*-
"""
    手动构造request对象测试视图
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test import RequestFactory

from node_man.views import HomeViewSet

User = get_user_model()

home = HomeViewSet.as_view({'get': 'index'})


class RequestTestCase(TestCase):
    """测试类"""

    def setUp(self):
        """初始化数据
        """

        self.factory = RequestFactory()
        self.uin = '12345'
        self.skey = 'test'

        self.user = User.objects.create_user(username=self.uin)

    def test_get(self):
        """测试样例
        """
        request = self.factory.get('/api/get_info/')
        print request

        # 设置cookies
        request.COOKIES = {
            'uin': self.uin,
            'skey': self.skey
        }

        resp = home(request)
        print 'get_info', resp.content
        # 测试返回码
        self.assertEqual(resp.status_code, 200)

    def test_get_user_info(self):
        request = self.factory.get('/api/get_info/')
        print request

        # 设置user对象
        request.user = self.user

        resp = home(request)
        print 'test_get_user_info', resp.content
        # 测试返回码
        # self.assertEqual(resp.status_code, 200)
