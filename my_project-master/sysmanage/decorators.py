# -*- coding: utf-8 -*-

from functools import wraps
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import available_attrs
from django.contrib.auth.models import Group
from rest_framework.exceptions import PermissionDenied
from common.log import logger


def surperuser_required(view_func):
    """
    装饰器检查当前用户是不是超级管理员
    """

    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied(detail=u'该用户没有该权限功能')

    return wrapper


def log(operated_object, operated_type, content, attr='', level='info'):
    """
    记录操作日志
    :param operated_object: 操作对象
    :param operated_type: 操作类型
    :param content: 操作内容
    :param is_success: 操作是否成功
    :param attr: response的data字典的key
    :param level 日志级别
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapper(request, *args, **kwargs):
            request.META['LOG_NEED'] = True
            request.META['LOG_INFO'] = {
                'operator': request.user.username,
                'operated_object': operated_object,
                'operated_type': operated_type,
                'content': content,
                'attr': attr,
                'level': level
            }
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


class SetDefaultGroup(object):
    """
    设置默认角色装饰器
    """

    def __init__(self, group_name):
        """
        :param group_name: 默认角色名
        """
        self.group_name = group_name

    def __call__(self, view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def wrapper(request, *args, **kwargs):
            try:
                user = request.user
                groups = user.groups.all()

                # 既不是APP管理员又没有分配任何角色
                if not user.is_superuser and not groups:
                    default_group = Group.objects.get(name=self.group_name)
                    user.groups.add(default_group)
            except Exception as e:
                logger.exception(_(u'用户【%s】设置默认角色【%s】出错。 %s' % (request.user.username, self.group_name, e)))

            return view_func(request, *args, **kwargs)

        return wrapper

set_default_group = SetDefaultGroup




