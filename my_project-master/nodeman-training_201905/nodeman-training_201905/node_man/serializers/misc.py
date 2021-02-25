# _*_ coding: utf-8 _*_
import re

from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.fields import empty

from node_man.constants import (ProcStateType, PROC_STATUS_DICT,
                                CATEGORY_CHOICES, CONFIG_FILE_FORMAT_CHOICES,
                                PLUGIN_OS_CHOICES, CPU_CHOICES)
from node_man.models import (
    Cloud, KV, Host, GsePluginDesc, Packages, ProcControl)
from .validators import CloudNameExistedValidator

CLOUD_PATTERN = re.compile(u"^[\w\u4e00-\u9fa5]{1,32}$")


class CloudSerializer(serializers.ModelSerializer):
    """云区域管理"""

    id = serializers.IntegerField(required=False)
    is_visible = serializers.BooleanField(required=False)
    bk_biz_id = serializers.CharField(min_length=1, max_length=12,
                                      required=False)
    bk_cloud_name = serializers.CharField(max_length=45, required=True)

    creator = serializers.CharField(required=False)
    bk_cloud_id = serializers.CharField(required=False)
    bk_supplier_id = serializers.CharField(min_length=1, max_length=12,
                                           required=False)

    def __init__(self, instance=None, data=empty, **kwargs):
        self.related_biz_id = 0
        if 'related_biz_id' in kwargs:
            self.related_biz_id = kwargs.get("related_biz_id", "")
            kwargs.pop('related_biz_id')
        self.validators = [CloudNameExistedValidator(self.related_biz_id)]
        super(CloudSerializer, self).__init__(instance=instance, data=data,
                                              **kwargs)

    def validate_bk_cloud_name(self, value):
        """校验云区域名称"""
        if not CLOUD_PATTERN.match(value):
            raise serializers.ValidationError(
                _(u"云区域名称不符合要求，长度小于32,中英文、数字和下划线"))
        return value

    def to_representation(self, instance):
        data = super(CloudSerializer, self).to_representation(instance)
        total_hosts = Host.objects.filter(
            is_deleted=False,
            bk_cloud_id=instance.bk_cloud_id,
            bk_biz_id=self.related_biz_id)
        proc_status_dict = {v: k for k, v in PROC_STATUS_DICT.iteritems()}
        data["hosts"] = {
            ProcStateType.UNKNOWN: total_hosts.filter(
                agent_status=proc_status_dict[ProcStateType.UNKNOWN]).count(),
            ProcStateType.RUNNING: total_hosts.filter(
                agent_status=proc_status_dict[ProcStateType.RUNNING]).count(),
            ProcStateType.TERMINATED: total_hosts.filter(
                agent_status=proc_status_dict[
                    ProcStateType.TERMINATED]).count()}
        data["enable_delete"] = not Host.objects.filter(
            is_deleted=False,
            bk_cloud_id=instance.bk_cloud_id).exists()
        return data

    class Meta:
        model = Cloud
        fields = (
            'id', 'creator', 'bk_biz_id', 'bk_supplier_id', 'bk_cloud_name',
            'bk_cloud_id', 'is_visible')


class KvSerializer(serializers.ModelSerializer):
    """配置表序列化类"""

    SPECIAL_KEYS = {
        'nginx': ['inner_url', 'outer_url'],
        'timeout': ['timeout'],
        'gse': ['inner_ip', 'outer_ip']
    }

    key = serializers.CharField(min_length=1, max_length=12, required=True)
    v_json = serializers.JSONField(required=True)

    class Meta:
        model = KV
        fields = ('key', 'v_json')

    def to_internal_value(self, data):
        key = data.get('key')
        data = {"key": key,
                'v_json': {
                    k: v
                    for k, v in data.iteritems() if
                    k in self.SPECIAL_KEYS.get(key)
                }}
        return super(KvSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        instance, created = self.Meta.model.objects.update_or_create(
            **validated_data)
        return instance


class GsePluginSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=32)
    description = serializers.CharField(required=False, max_length=128)
    scenario = serializers.CharField(required=False, max_length=256)
    description_en = serializers.CharField(required=False, max_length=128)
    scenario_en = serializers.CharField(required=False, max_length=256)
    category = serializers.ChoiceField(required=False, choices=CATEGORY_CHOICES)

    config_file = serializers.CharField(required=False, max_length=128, allow_null=True, allow_blank=True)
    config_format = serializers.ChoiceField(required=False, choices=CONFIG_FILE_FORMAT_CHOICES, allow_null=True, allow_blank=True)

    use_db = serializers.BooleanField(required=False)
    is_binary = serializers.BooleanField(required=False)
    auto_launch = serializers.BooleanField(required=False)

    class Meta:
        model = GsePluginDesc
        fields = (
            'id', 'name', 'description', 'description_en',
            'scenario', 'scenario_en', 'category',
            'config_file', 'config_format',
            'use_db', 'is_binary', 'auto_launch')

    def create(self, validated_data):
        data = {
            "name": validated_data["name"]
        }
        gse_plugin, created = GsePluginDesc.objects.update_or_create(
            defaults=validated_data,
            **data)
        return gse_plugin


class ProcessPackageSerializer(serializers.ModelSerializer):
    """
    插件更新包信息表
    """
    pkg_name = serializers.CharField(required=False, max_length=128)
    version = serializers.CharField(required=False, max_length=128)
    module = serializers.CharField(required=False, max_length=32)
    project = serializers.CharField(required=False, max_length=128)
    pkg_size = serializers.IntegerField(required=False)
    pkg_path = serializers.CharField(required=False, max_length=128)
    md5 = serializers.CharField(required=False, max_length=32)
    pkg_mtime = serializers.CharField(required=False, max_length=48)
    pkg_ctime = serializers.CharField(required=False, max_length=48)
    location = serializers.CharField(required=False, max_length=512)
    os = serializers.ChoiceField(required=False, choices=PLUGIN_OS_CHOICES)
    cpu_arch = serializers.ChoiceField(required=False, choices=CPU_CHOICES)

    class Meta:
        model = Packages
        fields = (
            'id', 'pkg_name', 'version',
            'module', 'project',
            'pkg_size', 'pkg_path',
            'md5', 'pkg_mtime', 'pkg_ctime', 'location', 'os', 'cpu_arch')

    def create(self, validated_data):
        data = {
            "module": validated_data["module"],
            "project": validated_data["project"],
            "version": validated_data["version"],
            "os": validated_data["os"],
            "cpu_arch": validated_data["cpu_arch"],
        }
        process_package, created = Packages.objects.update_or_create(
            defaults=validated_data,
            **data)
        return process_package


class ProcessControlInfoSerializer(serializers.ModelSerializer):
    module = serializers.CharField(required=False, max_length=32)
    project = serializers.CharField(required=False, max_length=32)

    install_path = serializers.CharField(required=False, max_length=128)
    log_path = serializers.CharField(required=False, max_length=128)
    data_path = serializers.CharField(required=False, max_length=128)
    pid_path = serializers.CharField(required=False, max_length=128)
    start_cmd = serializers.CharField(required=False, max_length=128)
    stop_cmd = serializers.CharField(required=False, max_length=128)
    restart_cmd = serializers.CharField(required=False, max_length=128)
    reload_cmd = serializers.CharField(required=False, max_length=128)

    kill_cmd = serializers.CharField(required=False, max_length=128)
    version_cmd = serializers.CharField(required=False, max_length=128)
    health_cmd = serializers.CharField(required=False, max_length=128)

    os = serializers.ChoiceField(required=False, choices=PLUGIN_OS_CHOICES)

    class Meta:
        model = ProcControl
        fields = (
            'id', 'module', 'project',
            'install_path', 'log_path', 'data_path', 'pid_path',
            'start_cmd', 'stop_cmd', 'restart_cmd', 'reload_cmd',
            'kill_cmd', 'version_cmd', 'health_cmd',
            'os')

    def create(self, validated_data):
        data = {
            "module": validated_data["module"],
            "project": validated_data["project"],
            "os": validated_data["os"],
        }
        process_info, created = ProcControl.objects.update_or_create(
            defaults=validated_data,
            **data)
        return process_info


class PluginSerializer(serializers.Serializer):
    gseplugindesc = GsePluginSerializer()
    packages = ProcessPackageSerializer()
    proccontrol = ProcessControlInfoSerializer()
