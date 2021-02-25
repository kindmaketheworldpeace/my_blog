# _*_ coding: utf-8 _*_

from .validators import *
from node_man.constants import (PLUGIN_OS_CHOICES, CPU_CHOICES)

class GsePluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = GsePluginDesc
        fields = '__all__'


class PluginReqSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, max_length=128)
    scenario = serializers.CharField(required=False, max_length=256)
    category = serializers.CharField(required=False, max_length=32)
    config_file = serializers.CharField(required=False, max_length=128)
    config_format = serializers.CharField(required=False, max_length=32)
    use_db = serializers.BooleanField(required=False)
    auto_launch = serializers.BooleanField(required=False)
    is_binary = serializers.BooleanField(required=False)

    def run_validation(self, data=None):
        self.validators = [
            PluginExistValidator()
        ]
        return super(PluginReqSerializer, self).run_validation(data)


class PackageReqSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    pkg_name = serializers.CharField(required=False, max_length=128)
    version = serializers.CharField(required=False, max_length=128)
    module = serializers.CharField(required=False, max_length=32)
    project = serializers.CharField(required=False, max_length=32)
    pkg_size = serializers.IntegerField(required=False)
    pkg_path = serializers.CharField(required=False, max_length=128)
    md5 = serializers.CharField(required=False, max_length=32)
    pkg_mtime = serializers.CharField(required=False, max_length=48)
    pkg_ctime = serializers.CharField(required=False, max_length=48)
    location = serializers.CharField(required=False, max_length=512)
    os = serializers.ChoiceField(required=False, choices=PLUGIN_OS_CHOICES)
    cpu_arch = serializers.ChoiceField(required=False, choices=CPU_CHOICES)


class ControlReqSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
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

class OptionReqSerializer(serializers.Serializer):
    keep_config = serializers.BooleanField(required=True)
    no_restart = serializers.BooleanField(required=True)
    no_delegate = serializers.BooleanField(required=True)


class ConfigsSerializer(serializers.Serializer):
    inner_ips = serializers.ListField(required=False)
    content = serializers.CharField(required=True)


class GlobalParamsSplitSerializer(serializers.Serializer):
    plugin = PluginReqSerializer(required=True)

    package = PackageReqSerializer(required=False)
    option = OptionReqSerializer(required=False)
    upgrade_type = serializers.CharField(required=False)
    configs = ConfigsSerializer(required=False, many=True)



class GlobalParamsSerializer(serializers.Serializer):
    plugin = PluginReqSerializer(required=True)

    package = PackageReqSerializer(required=False)
    control = ControlReqSerializer(required=False)
    option = OptionReqSerializer(required=False)
    upgrade_type = serializers.CharField(required=False)
    configs = ConfigsSerializer(required=False, many=True)

    def to_representation(self, instance):
        if instance:
            instance = json.loads(instance)
        return instance
