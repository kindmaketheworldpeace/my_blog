# -*- coding: utf-8 -*-
"""
全平台 esb-sdk 封装，依赖于 esb-sdk 包，但不依赖 sdk 的版本。
sdk 中有封装好 cc.get_app_by_user 方法时，可直接按以前 sdk 的习惯调用

>>> from blueapps.utils import client
>>> client.cc.get_app_by_user()

>>> from blueapps.utils import backend_client
>>> b_client = backend_client(access_token="oz1JdF5mBFDMyEQS812zlqrIBme3Kg")
>>> b_client.cc.get_app_by_user()

当前版本 sdk 中未封装好，但 api 已经有 get_app_by_user 的时候。需要指定请求方法
>>> client.cc.get_app_by_user.get()
"""
import warnings

from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from django.conf import settings
from node_man.utils.local import local
from node_man.component.request_middlewares import get_request

__all__ = [
    'client', 'backend_client', 'get_client_by_user', 'get_client_by_request'
]

# 开发者可以自己配置seb的sdk包名及需要的版本号，
# 配置了版本号，会比较框架加载的版本，如果低于配置的版本号，会打印一个警告。
ESB_SDK_VERSION = getattr(settings, "ESB_SDK_VERSION", "")
ESB_SDK_NAME = getattr(settings, "ESB_SDK_NAME")
ESB_API_PREFIX = getattr(settings, "ESB_API_PREFIX")


class SDKClient(object):
    sdk_package = None

    @property
    def __version__(self):
        return self.sdk_package.__version__

    @property
    def __backend__(self):
        return self.sdk_package.__name__

    def __new__(cls, **kwargs):
        if cls.sdk_package is None:
            try:
                cls.sdk_package = __import__(ESB_SDK_NAME,
                                             fromlist=['shortcuts'])
            except ImportError, e:
                raise ImportError("%s is not installed: %s"
                                  % (ESB_SDK_NAME, e))
        return super(SDKClient, cls).__new__(cls)

    def __init__(self, **kwargs):
        self.mod_name = ""
        self.sdk_mod = None
        self.common_args = kwargs
        if ESB_SDK_VERSION:
            from pkg_resources import SetuptoolsVersion
            if (SetuptoolsVersion(ESB_SDK_VERSION) >
                    SetuptoolsVersion(self.__version__)):
                warnings.warn('The current environment loaded sdk version(%s) '
                              'is lower than settings.ESB_SDK_VERSION(%s)' %
                              (self.__version__, ESB_SDK_VERSION),
                              stacklevel=2)

    def __getattr__(self, item):
        if not self.mod_name:
            ret = SDKClient(**self.common_args)
            ret.mod_name = item
            ret.setup_modules()
            if callable(ret.sdk_mod):
                return ret.sdk_mod
            return ret
        else:
            # 真实sdk调用入口
            ret = getattr(self.sdk_mod, item, None)
            if ret is None:
                ret = CollectionsCustom(self).add_api(item)
        if callable(ret):
            pass
            # print self.mod_name, "->", item
        else:
            ret = self
        return ret

    def setup_modules(self):
        self.sdk_mod = getattr(self.sdk_client, self.mod_name, None)
        if self.sdk_mod is None:
            self.sdk_mod = CollectionsCustom(self)

    def set_common_args(self, dict_kwargs=None, **kwargs):
        dict_kwargs = dict_kwargs or {}
        dict_kwargs.update(kwargs)
        self.common_args = dict_kwargs
        return self

    @property
    def sdk_client(self):
        try:
            request = get_request()
            # 调用sdk方法获取sdk client
            return self.load_sdk_class(
                "shortcuts", "get_client_by_request")(request)
        except:
            if hasattr(local, 'username') and local.username:
                return self.load_sdk_class(
                    "client", "ComponentClient"
                )(
                    app_code=settings.APP_CODE,
                    app_secret=settings.SECRET_KEY,
                    common_args=get_client_by_user(local.username).common_args
                )
            else:
                if settings.RUN_MODE != "DEVELOP":
                    raise Exception(
                        "sdk can only be called through the Web request, "
                        "use `get_client_by_user` to get client object")
                last_login_user = get_user_model().objects.all().order_by(
                    "-last_login")[0]
                return self.load_sdk_class(
                    "client", "ComponentClient"
                )(
                    app_code=settings.APP_CODE,
                    app_secret=settings.SECRET_KEY,
                    common_args=dict(
                        uin=last_login_user.username,
                    )
                )

    def load_sdk_class(self, mod, attr_or_class):
        dotted_path = "%s.%s.%s" % (self.__backend__, mod, attr_or_class)
        return import_string(dotted_path)

    def patch_sdk_component_api_class(self):

        def get_mod_name(api_obj):
            _mod_name = u"未知"
            with ignored(Exception):
                _mod_name = api_obj.url.split(ESB_API_PREFIX)[1].split("/")[0]
            return _mod_name

        def patch_get_item(self, item):
            method = item.upper()
            if method not in self.allowed_methods:
                raise Exception("esb api does not support method: %s" %
                                method)
            self.method = method
            return self

        def patch_call(self, *args, **kwargs):
            mod_name = get_mod_name(self)
            try:
                resp = call(self, *args, **kwargs)
            except ComponentAPIException, e:
                e.error_message = u"【模块：%s】接口返回结果异常：%s" % (mod_name, e.error_message)
                e.resp = None
                raise e
            with ignored(Exception):
                if not resp['result']:
                    message = resp.get('message') or u"未返回信息"
                    resp['message'] = u"【模块：%s】接口返回结果错误：%s" % (mod_name, message)
            return resp

        ComponentAPIException = self.load_sdk_class("exceptions", "ComponentAPIException")
        api_cls = self.load_sdk_class("base", "ComponentAPI")
        call = api_cls._call
        setattr(api_cls, "allowed_methods", CustomComponentAPI.allowed_methods)
        setattr(api_cls, "__getattr__", patch_get_item)
        setattr(api_cls, "_call", patch_call)


class CollectionsCustom(object):
    mod_map = dict()

    def __new__(cls, sdk_client, *args, **kwargs):
        if sdk_client.mod_name not in cls.mod_map:
            cls.mod_map[sdk_client.mod_name] = super(
                CollectionsCustom, cls).__new__(cls)
        return cls.mod_map[sdk_client.mod_name]

    def __init__(self, sdk_client):
        self.client = sdk_client

    def add_api(self, action):
        custom_api = CustomComponentAPI(self, action)
        setattr(self, action, custom_api)
        return custom_api

    def __getattr__(self, item):
        api = self.add_api(item)
        return api


class CustomComponentAPI(object):
    allowed_methods = ["GET", "POST"]

    def __init__(self, collection, action):
        self.collection = collection
        self.action = action

    def __getattr__(self, method):
        method = method.upper()
        if method not in self.allowed_methods:
            raise Exception("esb api does not support method: %s" % method)
        api_cls = self.collection.client.load_sdk_class("base", "ComponentAPI")
        return api_cls(
            client=SDKClient(**self.collection.client.common_args),
            method=method,
            path='{api_prefix}{collection}/{action}/'.format(
                api_prefix=ESB_API_PREFIX,
                collection=self.collection.client.mod_name,
                action=self.action
            ),
            description='custom api(%s)' % self.action
        )

    def __call__(self, *args, **kwargs):
        raise NotImplementedError(
            'custom api `%s` must specify the request method' % self.action)


client = SDKClient()
backend_client = SDKClient
if __name__ != "__main__":
    client.patch_sdk_component_api_class()


def get_client_by_user(user_or_username):
    user_model = get_user_model()
    if isinstance(user_or_username, user_model):
        username = user_or_username.username
    else:
        username = user_or_username
    return backend_client(uin=username)


def get_client_by_request(request=None):
    return client
