# -*- coding: utf-8 -*-
"""
权限校验类

class XxxPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user

"""
from django.core.cache import cache
from django.utils.translation import ugettext as _
from rest_framework import permissions

from node_man.component.cmdb import Business
from node_man.models import KV
from node_man.component.exceptions import NginxSettingError


class Permission(object):
    """
    权限控制类
    """

    @staticmethod
    def user_has_biz(username, bk_biz_id):
        """
        用户是否具有业务的权限
        """
        cache_key = '{}_has_biz_{}_perm'.format(username, bk_biz_id)
        perm = cache.get(cache_key)
        if perm is None:
            o_business = Business(bk_biz_id=bk_biz_id)
            perm = o_business.has_admin_auth(username)
            cache.set(cache_key, perm, 60)
        # return perm
        return True


class IsBizOwner(permissions.BasePermission):
    """
    业务所有者权限控制
    """
    message = u"您没有该业务的权限"

    def has_permission(self, request, view):
        bk_biz_id = view.kwargs.get('bk_biz_id')

        # 针对无biz_id的url，直接放行
        if bk_biz_id is None:
            return True
        username = request.user.username
        return Permission.user_has_biz(username, bk_biz_id)


class IsAdmin(permissions.BasePermission):
    """
    Nginx权限配置的鉴权
    """
    message = u"您没有操作nginx配置的权限"

    def has_permission(self, request, view):
        return request.user.is_superuser


class NginxSettingCheck(object):
    def has_permission(self, request, view):
        try:
            nginx_setting = KV.objects.get(key="nginx")
        except KV.DoesNotExist:
            raise NginxSettingError(_(u'nginx配置信息为空'))
        if not nginx_setting.v_json:
            raise NginxSettingError(_(u'nginx配置信息为空'))
        return True

    def has_object_permission(self, request, view, obj):
        return True
