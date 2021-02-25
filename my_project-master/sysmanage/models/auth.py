# -*- coding: utf-8 -*-
"""
鉴权models文件
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission


class PermissionGroup(models.Model):
    display_name = models.CharField(_(u'显示名称'), max_length=50)
    is_enable = models.BooleanField(_(u'是否启用'), default=True)

    class Meta:
        verbose_name = _(u'权限分组')
        verbose_name_plural = _(u'权限分组')

    def __unicode__(self):
        return self.display_name


class PermissionProfile(models.Model):
    display_name = models.CharField(_(u'显示名称'), max_length=50, blank=True)
    is_enable = models.BooleanField(_(u'是否启用'), default=True)
    permission = models.OneToOneField(Permission, verbose_name=_(u'权限'))
    permission_group = models.ForeignKey(PermissionGroup, verbose_name=_(u'权限分组'), on_delete=models.SET_NULL, null=True,
                                         blank=True)


class GroupProfile(models.Model):
    display_name = models.CharField(_(u'显示名称'), max_length=50, blank=True)
    is_enable = models.BooleanField(_(u'是否启用'), default=True)
    is_built_in = models.BooleanField(_(u'是否内置'), default=True)
    description = models.CharField(_(u'描述'), max_length=140, blank=True)
    group = models.OneToOneField(Group, verbose_name=_(u'组'))


class Menu(models.Model):
    name = models.CharField(_(u'名称'), max_length=50)
    display_name = models.CharField(_(u'显示名称'), max_length=50, blank=True)
    path = models.CharField(_(u'path地址'), max_length=50, blank=True)
    image_url = models.CharField(_(u'image地址'), max_length=50, blank=True)
    image_h_url = models.CharField(_(u'image高亮地址'), max_length=50, blank=True)
    icon = models.CharField(_(u'一级菜单图标'), max_length=255, null=True, blank=True)
    is_menu = models.BooleanField(_(u'是否为菜单'), default=False)
    remarks = models.TextField(_(u'备注信息'), blank=True)
    parent = models.ForeignKey('self', verbose_name=_(u'父级菜单'), null=True, blank=True)
    groups = models.ManyToManyField(Group, verbose_name=_(u'角色'), through="GroupToMenu", blank=True)
    created_by = models.CharField(_(u'创建者'), max_length=50, blank=True)
    create_date = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    updated_by = models.CharField(_(u'修改者'), max_length=50, blank=True)
    updated_date = models.DateTimeField(_(u'更新时间'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'菜单')
        verbose_name_plural = _(u'菜单')

    def __unicode__(self):
        return self.display_name


class GroupToMenu(models.Model):
    group = models.ForeignKey(Group, verbose_name=_(u'角色'))
    menu = models.ForeignKey(Menu, verbose_name=_(u'菜单'))
    created_by = models.CharField(_(u'创建者'), max_length=50, blank=True)
    create_date = models.DateTimeField(_(u'创建时间'), auto_now_add=True)
    remarks = models.TextField(_(u'备注信息'), blank=True)
    updated_by = models.CharField(_(u'修改者'), max_length=50, blank=True)
    updated_date = models.DateTimeField(_(u'更新时间'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'角色菜单中间表')
        verbose_name_plural = _(u'角色菜单中间表')

    def __unicode__(self):
        return u'%s_%s' % (self.group.name, self.menu.display_name)
