# _*_ coding: utf-8 _*_
import json
from copy import deepcopy
from datetime import datetime

from django.db import transaction
from django.db.models import Q
from rest_framework.fields import empty
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from node_man.models import Job, JobTask, TaskLog, GsePluginDesc
from node_man.constants import (JOB_CHOICES, NODE_CHOICES, OS_CHOICES, AUTH_CHOICES, STEP_CHOICES, FlagType,
                                JOB_TYPE_DICT, STEP_DISPLAY, StepType, NODE_TUPLE,
                                OS_TUPLE, ProcType, CODE_DESC_DICT)
from node_man.serializers.misc import GsePluginSerializer
from node_man.serializers.plugin_serializers import GlobalParamsSerializer, \
    GlobalParamsSplitSerializer
from .validators import *
from node_man.backend.scheduler import installer
from node_man.backend.manage_plugin.once_tasks import (
    manage_process, update_plugin, update_plugin_with_config)
from common.log import logger


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return value
        return self.choices.get(value, value)


class HostStatusSerializer(serializers.ModelSerializer):
    '''
    agent运行状态的序列化
    '''
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    version = serializers.CharField(required=False)

    class Meta:
        model = HostStatus
        fields = (
            'name',
            'status',
            'type',
            'version'
        )

    def to_representation(self, instance):
        data = super(HostStatusSerializer, self).to_representation(instance)
        data["host_id"] = instance.host.id
        data["is_deleted"] = instance.host.is_deleted
        data["version"] = data["version"] or "--"
        job_instance = instance.host.get_last_job_object()
        _job_serializer = BasicHostJobResultSerializer(job_instance)
        data["job_result"] = _job_serializer.data
        return data


class HostStatusReqSerializer(serializers.ModelSerializer):
    '''
    agent运行状态的序列化
    '''
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    proc_type = serializers.CharField(required=False)
    version = serializers.CharField(required=False)

    class Meta:
        model = HostStatus
        fields = (
            'name',
            'status',
            'proc_type',
            'version'
        )


class ThinHostSerializer(serializers.Serializer):
    '''
    主机列表序列化
    '''
    id = serializers.IntegerField(required=False)
    bk_biz_id = serializers.CharField(required=True)
    bk_cloud_id = serializers.CharField(required=True)
    inner_ip = serializers.CharField(required=True)
    outer_ip = serializers.CharField(required=False)
    node_type = serializers.CharField(required=False)
    os_type = serializers.CharField(required=False)
    has_cygwin = serializers.BooleanField(required=False)


class HostStatusFilterSerializer(serializers.Serializer):
    '''
    agent运行状态的序列化
    '''
    host = ThinHostSerializer(required=False)
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    proc_type = serializers.CharField(required=False)
    version = serializers.CharField(required=False)
    host__os_type = serializers.CharField(required=False)
    host__inner_ip = serializers.CharField(required=False)
    host__bk_cloud_id = serializers.CharField(required=False)


class HostFilterSerializer(serializers.Serializer):
    id__in = serializers.ListField(required=False)
    inner_ip__in = serializers.ListField(required=False)
    bk_cloud_id = serializers.CharField(required=False)
    node_type = serializers.CharField(required=False)

    status__name = serializers.CharField(required=False)
    status__version = serializers.CharField(required=False)
    status__proc_type = serializers.CharField(required=False)


class HostReqDataSerializer(HostFilterSerializer):
    '''
    主机列表请求参数序列化
    '''
    bk_set_id = serializers.CharField(required=False)
    bk_module_id = serializers.CharField(required=False)
    version = serializers.CharField(required=False)
    os_type = serializers.CharField(required=False)
    node_type = serializers.CharField(required=False)
    keyword = serializers.CharField(required=False)
    ip = serializers.CharField(required=False)
    order_by = serializers.CharField(required=False)
    object_type = serializers.CharField(required=False)
    ignore_page = serializers.CharField(required=False)

    def to_internal_value(self, data):
        data = data.copy()
        host_id_list = []
        if "version" in data:
            if not data["version"]:
                data.pop("version")
            else:
                querysets = HostStatus.objects.filter(name='gseagent', version__contains=data["version"])
                for item in querysets:
                    host_id_list.append(item.host.id)
        # bugfix: 默认object_type=agent
        if not data.has_key("object_type"):
            data["object_type"] = "agent"

        data = super(HostReqDataSerializer, self).to_internal_value(data)
        empty_data = [None, '', []]
        fields = self._writable_fields
        data["id__in"] = host_id_list
        for field in fields:
            if field.field_name in data and data[field.field_name] in empty_data:
                data.pop(field.field_name)
        return data


class HostCheckSerializer(serializers.Serializer):
    '''
    主机列表请求参数序列化
    '''
    bk_cloud_id = serializers.CharField(required=False)
    bk_supplierid = serializers.CharField(required=False)
    hosts = serializers.CharField(required=True)

    def to_internal_value(self, data):
        return super(HostReqDataSerializer, self).to_internal_value(data)


class HostSerializer(serializers.Serializer):
    '''
    主机列表序列化
    '''
    id = serializers.IntegerField(required=False)
    status = HostStatusSerializer(many=True, read_only=True)
    bk_biz_id = serializers.CharField(required=True)
    bk_cloud_id = serializers.CharField(required=True)
    bk_supplier_account = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bk_supplier_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    conn_ip = serializers.IPAddressField(required=True)
    cascade_ip = serializers.IPAddressField(required=False)
    login_ip = serializers.IPAddressField(required=False)
    cc_ip_types = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    data_ip = serializers.IPAddressField(required=False)
    node_type = serializers.ChoiceField(choices=NODE_CHOICES, required=False)
    os_type = serializers.ChoiceField(required=False, choices=OS_CHOICES)
    has_cygwin = serializers.BooleanField(required=False)
    account = serializers.CharField(required=False)
    port = serializers.IntegerField(required=False)
    auth_type = serializers.ChoiceField(required=False, choices=AUTH_CHOICES)
    password = serializers.CharField(required=False, allow_blank=True)
    key = serializers.CharField(required=False, allow_blank=True)
    update_time = serializers.DateTimeField(required=False)

    class Meta:
        model = Host
        fields = (
            'id',
            'status',
            'job_result',
            'bk_cloud_id',
            'bk_biz_id',
            'conn_ip',
            'cascade_ip',
            'node_type',
            'has_cygwin',
            'account',
            'auth_type',
            'password',
            'key',
            'os_type',
            'port',
            'update_time'
        )

    def create(self, validated_data):
        host_info = validated_data
        host_info["is_deleted"] = False
        # TODO: use conn_ip/cascade_ip rather than inner_ip/outer_ip

        conn_ip = host_info.pop("conn_ip", '')
        cascade_ip = host_info.pop("cascade_ip", '')
        host_info["inner_ip"] = conn_ip

        defaults = {"bk_cloud_id": host_info["bk_cloud_id"],
                    "bk_biz_id": host_info.get("bk_biz_id"),
                    'inner_ip': conn_ip,
                    'data_ip': host_info.get("data_ip", conn_ip),
                    'login_ip': host_info.get("login_ip", conn_ip),
                    'cc_ip_types': host_info.get("cc_ip_types", ''),
                    'is_deleted': False}
        if cascade_ip:
            defaults.update(outer_ip=cascade_ip)
            host_info["outer_ip"] = cascade_ip
        host, created = Host.objects.update_or_create(
            defaults=defaults, **host_info)
        if created:
            HostStatus.objects.create(host=host)
        return host

    def update(self, instance, validated_data):
        # TODO: use conn_ip/cascade_ip rather than inner_ip/outer_ip
        validated_data["inner_ip"] = validated_data.pop("conn_ip", '')
        cascade_ip = validated_data.pop("cascade_ip", '')
        if cascade_ip:
            validated_data["outer_ip"] = cascade_ip

        Host.objects.filter(id=instance.id).update(**validated_data)
        return instance

    def run_validation(self, data=empty):
        value = super(HostSerializer, self).run_validation(data)
        return value

    def to_internal_value(self, data):
        # if not data.get("op_type") in [OpType.INSTALL, None, OpType.IMPORT] and "node_type" in data:
        #     data.pop("node_type")
        if data.get("op_type") not in [OpType.UPDATE_AUTHINFO, None]:
            logger.info("update time %s" % datetime.now())
            data["update_time"] = datetime.now()
        return super(HostSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        # TODO: use conn_ip rahter than inner_ip in model
        instance.conn_ip = instance.inner_ip
        instance.cascade_ip = instance.outer_ip
        data = super(HostSerializer, self).to_representation(instance)
        object_type = self.context.get("request").query_params.get("object_type", "agent")
        _job = instance.get_last_job_object(object_type)
        _job_result_serializers = BasicHostJobResultSerializer(instance=_job)
        data["job_result"] = _job_result_serializers.data
        data["password"] = ""
        data["key"] = ""
        return data


class HostRelatedField(serializers.RelatedField):
    '''
    任务中主机列表字段
    '''

    def get_queryset(self):
        return self.queryset

    def to_representation(self, value):
        # serializer = HostSerializer(value)
        serializer = BreifHostSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        return data

    def run_validation(self, data=empty):
        # 清洗字段数据
        validate_data = HostSerializer().run_validation(data)
        try:
            host = Host.objects.get(bk_cloud_id=validate_data["bk_cloud_id"], inner_ip=validate_data['conn_ip'],
                                    is_deleted=False)
        except Host.DoesNotExist:
            host = None

        # 清洗自定义校验方法
        self.validators = [HostExistValidator(host), AgentTypeValidator(), HostJobStatusValidator(host)]
        if data.get("node_type") in NODE_TUPLE and (
                data.get("op_type") in [OpType.INSTALL, OpType.REINSTALL, OpType.UPGRADE]):
            self.validators.append(AuthValidator(host))

        super(HostRelatedField, self).run_validation(data)
        return validate_data


class BasicHostJobResultSerializer(serializers.Serializer):
    '''
    任务运行状态序列化基类，不包含主机的序列化
    '''
    job_id = serializers.CharField(max_length=45, required=False)
    status = serializers.CharField(max_length=45, default='test')
    err_code = serializers.CharField(max_length=45, default='')
    step = ChoiceField(choices=STEP_CHOICES, default='')
    err_code_desc = serializers.SerializerMethodField()

    class Meta:
        model = JobTask
        fields = (
            "job_id"
            "status",
            'err_code',
            'step',
        )

    def get_err_code_desc(self, instance):
        return CODE_DESC_DICT.get(instance.err_code)

    def to_representation(self, instance):
        data = super(BasicHostJobResultSerializer, self).to_representation(instance)
        data['step'] = u"%s(%s)" % (data['step'], JOB_TYPE_DICT.get(instance.job.job_type, ""))
        return data


class HostJobResultSerializer(BasicHostJobResultSerializer):
    '''
    包含host的任务结果序列化
    '''
    host = HostRelatedField(required=True)

    class Meta:
        model = JobTask
        fields = (
            "host",
            "status",
            'err_code',
            'step',
        )

    def create(self, validated_data):
        host = validated_data[0].get("host")
        job = validated_data[0].get("job")

        host_info = host["host"]
        filter_condition = {"bk_cloud_id": host_info["bk_cloud_id"],
                            'inner_ip': host_info.get("conn_ip"),
                            "is_deleted": False}
        try:
            host = Host.objects.get(**filter_condition)
        except Exception, e:
            host = None
        if job.job_type not in [JobType.UNINSTALL_AGENT, JobType.REMOVE_AGENT]:
            host_serializer = HostSerializer(instance=host, data=host_info)
            host_serializer.is_valid(raise_exception=True)
            host = host_serializer.save()

        JobTask.objects.create(job=job, host=host)

    def to_internal_value(self, data):
        """
        Dict of native values <- Dict of primitive datatypes.
        """
        try:
            return super(HostJobResultSerializer, self).to_internal_value(data)
        except ValidationError as exc:
            errors = exc.detail
            for key, value in errors.iteritems():
                if key != 'host':
                    continue
                if isinstance(value, (list, str)):
                    errors["host:%s" % data[key].get("inner_ip")] = {api_settings.NON_FIELD_ERRORS_KEY: value}
                elif isinstance(value, dict):
                    errors["host:%s" % data[key].get("inner_ip")] = value
                errors.pop(key)
                break
            raise ValidationError(errors)


class JobLogSerializer(serializers.Serializer):
    '''
    日志的序列化
    '''
    content = serializers.CharField(required=False)

    class Meta:
        model = TaskLog
        fields = (
            "content"
        )

    def to_representation(self, instance):
        data = super(JobLogSerializer, self).to_representation(instance)
        if instance.flag == FlagType.STEP:
            data["content"] = '<br/><b>>>step %s %s</b>' % (
                instance.index, STEP_DISPLAY.get(data["content"], data["content"]))
        else:
            data["content"] = '[%s]: %s' % (instance.create_time, data["content"])
        return data


class HostJobLogSerializer(BasicHostJobResultSerializer):
    '''
    单台机器的任务日志序列化
    '''

    def to_representation(self, instance):
        data = super(HostJobLogSerializer, self).to_representation(instance)
        logs = TaskLog.objects.filter(level__in=["user"]).filter(
            (Q(job_id=instance.job.id) & Q(job_task_id__isnull=True)) |
            Q(job_task_id=instance.id)).order_by("id")

        log_content = ""
        index = 0

        for log in logs:
            if log.flag == FlagType.STEP:
                index = index + 1
                log.index = index
            _serializer = JobLogSerializer(instance=log)
            log_content += "<pre>%s </pre>" % _serializer.data["content"]

        data["logs"] = log_content

        print log_content

        return data


class BreifHostSerializer(serializers.Serializer):
    '''
    主机列表序列化
    '''
    id = serializers.IntegerField(required=False)
    bk_biz_id = serializers.CharField(required=True)
    bk_cloud_id = serializers.CharField(required=True)
    inner_ip = serializers.IPAddressField(required=True)
    outer_ip = serializers.IPAddressField(required=False)
    node_type = serializers.ChoiceField(choices=NODE_CHOICES, required=False)
    os_type = serializers.ChoiceField(required=False, choices=OS_CHOICES)
    has_cygwin = serializers.BooleanField(required=False)

    class Meta:
        model = Host
        fields = (
            'id',
            'bk_cloud_id',
            'bk_biz_id',
            'inner_ip',
            'outer_ip',
            'node_type',
            'os_type',
            'has_cygwin',
        )


class HostTaskResultSerializer(BasicHostJobResultSerializer):
    '''
    包含host的任务结果序列化
    '''
    host = BreifHostSerializer(required=True)

    class Meta:
        model = JobTask
        fields = (
            "host",
            "status",
            'err_code',
            'step',
        )


class JobSerializer(serializers.ModelSerializer):
    '''
    任务类的参数序列化
    '''
    hosts = HostJobResultSerializer(many=True)
    creator = serializers.CharField(required=True)
    bk_biz_id = serializers.CharField(required=True)
    bk_cloud_id = serializers.CharField(required=True)
    job_type = serializers.ChoiceField(required=True, choices=JOB_CHOICES)
    # global_params = serializers.CharField(required=False)
    global_params = GlobalParamsSerializer(required=False, allow_null=True)
    bk_supplier_account = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    bk_supplier_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    status_count = serializers.SerializerMethodField()
    job_type_desc = serializers.SerializerMethodField()
    os_count = serializers.SerializerMethodField()
    host_count = serializers.SerializerMethodField()
    op_target = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = (
            "id",
            "creator",
            "bk_biz_id",
            "bk_supplier_account",
            "bk_supplier_id",
            "bk_cloud_id",
            "job_type",
            "hosts",
            "global_params",
            "start_time",
            "end_time",
            "status_count",
            "os_count",
            "host_count",
            "job_type_desc",
            "op_target",
        )

    def get_status_count(self, instance):
        hosts = instance.hosts.all()

        success_count = 0
        failed_count = 0
        running_count = 0

        for host in hosts:
            if host.status == StatusType.SUCCESS:
                success_count += 1
            elif host.status == StatusType.FAILED:
                failed_count += 1
            else:
                running_count += 1

        return dict(
            success_count=success_count,
            failed_count=failed_count,
            running_count=running_count,
        )

    def get_host_count(self, instance):
        hosts = instance.hosts.all()
        return len(hosts)

    def get_os_count(self, instance):
        hosts = instance.hosts.all()
        host_os = {os_type: 0 for os_type in OS_TUPLE}
        for host in hosts:
            if hasattr(OsType, host.host.os_type):
                host_os[host.host.os_type] += 1
        return host_os

    def get_op_target(self, instance):
        target = {
            "name": "",
            "config_file": "",
        }
        try:
            global_params = json.loads(instance.global_params)
            if global_params.has_key("plugin"):
                id = global_params.get("plugin").get("id")
                plugin = GsePluginDesc.objects.get(id=id)
                _serializer = GsePluginSerializer(plugin)
                return _serializer.data
            else:
                return target
        except Exception, e:
            return target

    def get_job_type_desc(self, instance):
        job_type = instance.job_type

        if job_type == JobType.UPDATE_AUTHINFO:
            return JOB_TYPE_DICT.get(job_type, job_type)
        return JOB_TYPE_DICT.get(job_type, job_type) + job_type.split("_")[1]

    def to_internal_value(self, data):
        # 在这里对data做分类
        hosts = []
        if data['op_type'] in [OpType.UNINSTALL, OpType.REMOVE]:
            data["job_node_type"] = NodeType.AGENT
        if data['op_type'] in [OpType.UPDATE_AUTHINFO, 'SAVE']:
            data['op_type'] = OpType.UPDATE_AUTHINFO
            data["job_node_type"] = NodeType.AGENT
        for host in data.get('hosts'):
            inner_ips = host.get("conn_ips", "").split(",")
            host.pop("conn_ips", '')

            for ip in inner_ips:
                new_host = {
                    "conn_ip": ip,
                    "bk_biz_id": data["bk_biz_id"],
                    "bk_cloud_id": data.get("bk_cloud_id", "0"),
                    "op_type": data["op_type"],
                    "bk_supplier_account": data["bk_supplier_account"],
                    "bk_supplier_id": data["bk_supplier_id"]
                }
                if data["node_type"] in NODE_TUPLE:
                    new_host.update(node_type=data["node_type"])
                new_host.update(host)
                hosts.append({"host": new_host})
        job_type = "%s_%s" % (data["op_type"], data.get("job_node_type") or data['node_type'])
        data.update({
            "hosts": hosts,
            "job_type": JobType.UPDATE_AUTHINFO if data['op_type'] == JobType.UPDATE_AUTHINFO else job_type
        })

        return super(JobSerializer, self).to_internal_value(data)

    def run_validation(self, data=None):
        self.validators = [
            JobTypeValidator(),
            NodeTypeRelationValidator(),
            CloudExistedValidator(),
            HostInstalledValidator(data.get("ignore_installed_elsewhere", False))
        ]

        if data.get("node_type") == ProcType.PLUGIN:
            self.validators += [
                GlobalParmasExistValidator()
            ]
        return super(JobSerializer, self).run_validation(data)

    def create(self, validated_data):
        # global_parmas以字符串方式存储
        if validated_data.has_key("global_params"):
            global_params = validated_data.pop('global_params')
            validated_data["global_params"] = json.dumps(global_params)
        host_list = deepcopy(validated_data.get("hosts"))
        # 创建job
        validated_data.pop('hosts')
        win_hosts = []
        linux_hosts = []

        # 拆分卸载组,根据linux和windows机器进行拆分
        if validated_data["job_type"] in [JobType.UNINSTALL_AGENT, JobType.REMOVE_AGENT]:
            for host in host_list:
                if Host.get_os_type(host['host'], validated_data["bk_cloud_id"]) == OsType.WINDOWS:
                    win_hosts.append(host)
                else:
                    linux_hosts.append(host)
        else:
            linux_hosts = host_list
        # 卸载任务区分windows和linux，需要创建两个任务
        if linux_hosts:
            job = self.perform_create(validated_data, linux_hosts, kwargs={'os_type': OsType.LINUX})
        if win_hosts:
            job = self.perform_create(validated_data, win_hosts, kwargs={'os_type': OsType.WINDOWS})
        return job

    def perform_create(self, validated_data, host_list, kwargs=None):
        if kwargs is None:
            kwargs = {}
        with transaction.atomic():
            job = Job.objects.create(**validated_data)
            # 创建或更新host 创建result
            self.fields.fields['hosts'].create([{"job": job, "host": host}] for host in host_list)

        # 不需要创建后台任务
        if validated_data["job_type"] in [JobType.UPDATE_AUTHINFO, JobType.IMPORT_PROXY,
                                          JobType.IMPORT_AGENT, JobType.IMPORT_PAGENT]:
            job.update_status(status=StatusType.SUCCESS)
            return job

        # 创建后台任务
        if validated_data["job_type"] in [
            JobType.START_PLUGIN,
            JobType.STOP_PLUGIN,
            JobType.RELOAD_PLUGIN,
            JobType.RESTART_PLUGIN,
            JobType.DELEGATE_PLUGIN,
            JobType.UNDELEGATE_PLUGIN,
        ]:
            celery_task = manage_process.apply_async((job.id,), kwargs=kwargs)
        elif validated_data["job_type"] in [
            JobType.UPGRADE_PLUGIN,
        ]:
            celery_task = update_plugin.apply_async((job.id,), kwargs=kwargs)
        elif validated_data["job_type"] in [
            JobType.UPDATE_PLUGIN,
        ]:
            celery_task = update_plugin_with_config.apply_async((job.id,), kwargs=kwargs)
        else:
            celery_task = installer.apply_async((job.id,), kwargs=kwargs)

        job.update_task_id(str(celery_task.task_id))
        return job


class LogSerializer(serializers.Serializer):
    '''
    日志的序列化
    '''
    id = serializers.IntegerField(required=False)
    content = serializers.SerializerMethodField()
    level = serializers.CharField(max_length=45)
    flag = serializers.CharField(max_length=45)
    create_time = serializers.DateTimeField()
    job_task_id = serializers.IntegerField()
    job_id = serializers.IntegerField()

    class Meta:
        model = TaskLog
        fields = (
            "id",
            "content",
            "level",
            "flag",
            "create_time",
            "job_task_id",
            "job_id"
        )

    def get_content(self, instance):
        if instance.flag == FlagType.STEP:
            return STEP_DISPLAY.get(instance.content, instance.content)
        return instance.content


class JobFilterSerializer(serializers.Serializer):
    start_time__gte = serializers.DateField(required=False)
    start_time__lte = serializers.DateField(required=False)
    bk_cloud_id = serializers.CharField(required=False)
    job_type = serializers.CharField(required=False)


class HostSplitSerializer(serializers.Serializer):
    '''
    主机列表序列化
    '''

    bk_biz_id = serializers.CharField(required=True)
    bk_cloud_id = serializers.CharField(required=True)
    inner_ip = serializers.IPAddressField(required=True)


class JobSplitSerializer(serializers.Serializer):
    hosts = HostSplitSerializer(many=True)
    creator = serializers.CharField(required=True)
    bk_biz_id = serializers.CharField(required=True)
    bk_cloud_id = serializers.CharField(required=True)
    op_type = serializers.CharField(required=True)
    node_type = serializers.CharField(required=True)
    # global_params = serializers.CharField(required=False)
    global_params = GlobalParamsSplitSerializer(required=False, allow_null=True)

    def run_validation(self, data=None):
        self.validators = [
            GlobalParmasExistValidator(),
            OsPluginValidator()
        ]
        return super(JobSplitSerializer, self).run_validation(data)

    def to_internal_value(self, data):
        # 在这里对data做分类
        hosts = []
        for host in data.get('hosts'):
            inner_ips = host.get("conn_ips", "").split(",")
            for ip in inner_ips:
                new_host = {
                    "inner_ip": ip,
                    "bk_biz_id": data["bk_biz_id"],
                    "bk_cloud_id": data.get("bk_cloud_id", "0"),
                }
                hosts.append(new_host)
        data.update({
            "hosts": hosts,
        })
        return super(JobSplitSerializer, self).to_internal_value(data)
