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

from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    是否为APP管理员
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `creator`.
        return obj.creator == request.user
