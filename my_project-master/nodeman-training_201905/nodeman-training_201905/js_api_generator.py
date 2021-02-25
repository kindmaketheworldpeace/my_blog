# -*- coding: utf-8 -*-
"""
生成前端API调用函数
"""

import os
import abc
import six
import uuid

from StringIO import StringIO
from collections import namedtuple
from importlib import import_module
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet
from django.template import engines
from django.conf import settings


# 需要扫描的视图
ACTIVE_VIEWS = {
    
    "node_man": {
        "api": "node_man.views",
    }
}

django_engine = engines['django']


TEMPLATE = u"""/**
 * @module: resources.js
 * @author: 蓝鲸智云
 * @create: {% now 'Y-m-d H:i:s' %}
 */

var BaseRestAPI = function (method, url, data, options) {
    // 所有请求默认加上bk_biz_id
    if (data) {
        data.bk_biz_id = data.bk_biz_id || cc_biz_id
    } else {
        data = {
            bk_biz_id: cc_biz_id
        }
    }
    var defaultOptions = {
        type: method,
        url: site_url + url,
        dataType: 'json',
    }
    if (method === 'GET') {
        defaultOptions.data = data
    } else {
        defaultOptions.data = JSON.stringify(data)
        defaultOptions.contentType = 'application/json'
    }
    return $.ajax(Object.assign(defaultOptions, options))
}

/*
  列表类型的API
 */
var RestListAPI = function(method, url) {
    return function (data, options) {
        return BaseRestAPI(method, url, data, options)
    }
}


/*
  详情类型的API，需要替换掉URL字符串模版中的"{pk}"，以生成合法的URL
 */
var RestDetailAPI = function(method, url) {
    return function (id, data, options) {
        var requestURL = url.replace("{pk}", id)
        return BaseRestAPI(method, requestURL, data, options)
    }
}

/* Model API */
var Model = {
    {% for model in models %}
    {{ model.name }}: {
        {% for method in model.methods %}
        /**
         * {% if method.api_description %}@apiDescription {{ method.api_description | safe }}{% endif %}
         * @api { {{ method.method }} } {{ method.url }} {{ method.api_name }}
         * @apiName {{ method.api_name }}  
         * @apiGroup {{ model.name }}  
         */
        {{ method.function_name }}: {% if method.is_detail %}RestDetailAPI{% else %}RestListAPI{% endif %}("{{ method.method }}", "{{ method.request_url | safe }}"),
        {% endfor %}
    },
    {% endfor %}
}
"""

template = django_engine.from_string(TEMPLATE)


def get_underscore_viewset_name(viewset):
    return camel_to_underscore(viewset.__name__.replace("ViewSet", ""))


def camel_to_underscore(camel_str):
    assert isinstance(camel_str, six.string_types)

    buf = StringIO()
    str_len = len(camel_str)

    for i in range(str_len):
        cur_letter = camel_str[i]
        if i and cur_letter == cur_letter.upper():
            prev_letter = camel_str[i - 1]
            next_letter = camel_str[i + 1] if i < str_len - 1 else "A"
            if cur_letter.isalpha():
                if prev_letter != prev_letter.upper() \
                        or next_letter != next_letter.upper():
                    buf.write('_')
        buf.write(cur_letter)

    result = buf.getvalue()
    buf.close()

    return result.lower()


def underscore_to_camel(underscore_str):
    assert isinstance(underscore_str, six.string_types)

    return ''.join(map(lambda x: x.capitalize(), underscore_str.split('_')))


def uniqid():
    # 不带横杠
    return uuid.uuid3(
        uuid.uuid1(),
        uuid.uuid4().hex
    ).hex


def generate_js_api():
    """
    主入口
    """
    models = []
    for app_name, view_modules in ACTIVE_VIEWS.items():
        for view_name, view_path in view_modules.items():
            views = import_module(view_path)
            model_context = _generate_js_api_by_module(views, app_name)
            models += model_context

    code = template.render({
        "models": models,
    })
    with open(os.path.join(settings.STATICFILES_DIRS[0], "js", "resources.js"), "w+") as fp:
        fp.write(code)


def _generate_js_api_by_module(views, app_name=""):
    model_api = []
    for attr, val in views.__dict__.iteritems():
        if attr[0].islower():
            continue
        if isinstance(val, type):
            if issubclass(val, GenericViewSet):
                model_api.append(GenericViewSetParser.parse(val, app_name))
    return model_api


class BaseParser(object):
    """
    ViewSet解析器基类，将viewset中的每一个view的url、method等属性解析出来
    """
    __metaclass__ = abc.ABCMeta

    ViewFunction = namedtuple('ViewFunction', ['method', 'is_detail'])

    default_view_functions = {
        'list': ViewFunction('GET', False),
        'create': ViewFunction('POST', False),
        'retrieve': ViewFunction('GET', True),
        'update': ViewFunction('PUT', True),
        'partial_update': ViewFunction('PATCH', True),
        'destroy': ViewFunction('DELETE', True),
    }

    class ViewNameFormat(object):
        default_list_route = '{basename}-list'
        custom_list_route = '{basename}-{methodnamehyphen}'
        default_detail_route = '{basename}-detail'
        custom_detail_route = '{basename}-{methodnamehyphen}'

    @classmethod
    def parse(cls, viewset_cls, app_name=""):
        raise NotImplementedError

    @staticmethod
    def replace_methodname(format_string, basename, methodname):
        """
        Partially format a format_string, swapping out any
        '{basename}' or '{methodnamehyphen}' components.
        """
        methodnamehyphen = methodname.replace('_', '-')
        ret = format_string
        ret = ret.replace('{basename}', basename)
        ret = ret.replace('{methodnamehyphen}', methodnamehyphen)
        return ret


class GenericViewSetParser(BaseParser):
    """
    GenericViewSet解析器
    """
    @classmethod
    def parse(cls, viewset_cls, app_name=""):
        viewset_name = get_underscore_viewset_name(viewset_cls)
        viewset_name_camel = underscore_to_camel(viewset_name)
        viewset_name_camel = viewset_name_camel[0].lower() + viewset_name_camel[1:]

        result = []
        for methodname in dir(viewset_cls):
            attr = getattr(viewset_cls, methodname)
            httpmethods = getattr(attr, 'bind_to_methods', None)
            if httpmethods:
                is_custom = True
                is_detail = getattr(attr, 'detail', True)
                httpmethod = httpmethods[0].upper()
            elif methodname in cls.default_view_functions:
                view_func = cls.default_view_functions[methodname]
                is_custom = False
                is_detail = view_func.is_detail
                httpmethod = view_func.method
            else:
                continue

            if is_custom:
                if is_detail:
                    url_name_format = cls.ViewNameFormat.custom_detail_route
                else:
                    url_name_format = cls.ViewNameFormat.custom_list_route
            else:
                if is_detail:
                    url_name_format = cls.ViewNameFormat.default_detail_route
                else:
                    url_name_format = cls.ViewNameFormat.default_list_route

            url_name = cls.replace_methodname(url_name_format, viewset_name, methodname)

            if app_name:
                url_name = "%s:%s" % (app_name, url_name)

            kwargs = {}
            pk_placeholder = uniqid()
            if is_detail:
                kwargs = {"pk": pk_placeholder}
            request_url = reverse(url_name, kwargs=kwargs).replace(pk_placeholder, "{pk}")

            api_name = underscore_to_camel(methodname)
            function_name = api_name[0].lower() + api_name[1:]

            api_description = attr.__doc__
            if api_description:
                api_description = api_description.decode("utf-8").strip()

            js_code_context = {
                "api_description": api_description,
                "url": request_url,
                "method": httpmethod,
                "api_name": api_name,
                "function_name": function_name,
                "request_url": request_url[1:],
                "is_detail": is_detail,
            }
            result.append(js_code_context)
        return {
            "name": viewset_name_camel,
            "methods": result,
        }
