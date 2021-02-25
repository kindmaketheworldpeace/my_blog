# -*- coding: utf-8 -*-
import copy
from django.db.models import Q, Count
from django.http import Http404
from django.utils.translation import ugettext as _
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from node_man.component.cmdb import Business
from node_man.component.exceptions import ParamError
from node_man.component.gse import GSEAgent
from node_man.component.viewsets import (ModelViewSet)
from node_man.constants import (ResponseCodeStatus, JobType, FlagType,
                                JOB_STEP_MAPPING, STEP_CHOICES, ProcType,
                                OpType)
from node_man.constants import StatusType
from node_man.models import (Job, Host, HostStatus, JobTask, GsePluginDesc,
                             Packages, ProcControl, TaskLog)
from node_man.serializers import (
    JobSerializer, HostSerializer, HostStatusSerializer,
    HostReqDataSerializer, HostJobLogSerializer, HostFilterSerializer,
    LogSerializer, HostTaskResultSerializer,
    JobFilterSerializer, HostStatusReqSerializer, HostStatusFilterSerializer,
    JobSplitSerializer)
from node_man.serializers.misc import (
    GsePluginSerializer, ProcessPackageSerializer,
    ProcessControlInfoSerializer)
from node_man.serializers.validators import BulkHostValidator


class JobViewSet(ModelViewSet):
    '''
    安装，重装，卸载，终止任务接口
    '''
    # minor: 倒序
    queryset = Job.objects.all().order_by("-id")
    serializer_class = JobSerializer
    request_serializer_class = JobFilterSerializer
    http_method_names = ["get", "post", 'delete']
    bk_biz_id = None
    operator = ''
    request_params = {}
    bk_supplier_account = None
    bk_supplier_id = None

    def get_queryset(self):
        if "start_time__gte" in self.request_params:
            start_time__gte = self.request_params.pop("start_time__gte")
            self.request_params[
                "start_time__gte"] = "%s 00:00:00" % start_time__gte
        if "start_time__lte" in self.request_params:
            start_time__lte = self.request_params.pop("start_time__lte")
            self.request_params[
                "start_time__lte"] = "%s 23:59:59" % start_time__lte

        return self.queryset.filter(
            bk_biz_id=self.bk_biz_id,
            is_canceled=False).filter(**self.request_params)

    def get_serializer(self, *args, **kwargs):
        creator = kwargs.get("data", {}).get("creator", "")
        kwargs.get("data", {}).update(
            {"bk_biz_id": self.bk_biz_id,
             "creator": self.operator or creator,
             "bk_supplier_account": self.bk_supplier_account,
             "bk_supplier_id": self.bk_supplier_id})
        return super(JobViewSet, self).get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        self.operator = request.user.username
        self.bk_supplier_account = getattr(request.user, "bk_supplier_account", "")
        self.bk_supplier_id = getattr(request.user, "bk_supplier_id", "0")
        kwargs["bk_supplier_account"] = self.bk_supplier_account
        kwargs["bk_supplier_id"] = self.bk_supplier_id
        return super(JobViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        _serializer = self.request_serializer_class(data=request.GET)
        _serializer.is_valid(raise_exception=True)
        self.request_params = _serializer.data
        return super(JobViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        return super(JobViewSet, self).retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()

    @list_route(methods=['post'], url_path='bulk')
    def bulk_destroy(self, request, *args, **kwargs):
        bk_cloud_id = request.data.get("bk_cloud_id")
        all_objs = self.queryset.filter(
            bk_cloud_id=bk_cloud_id, bk_biz_id=kwargs.get("bk_biz_id"))
        if not all_objs.exists():
            raise ParamError(_(u'当前云区域不存在执行中的任务'))
        for job in all_objs:
            self.perform_destroy(job)
        return Response()

    @list_route(methods=['get'], url_path='running_task_count')
    def get_num_of_running_task(self, request, bk_biz_id):
        bk_cloud_id = request.GET.get("bk_cloud_id", None)
        return Response({
            "running_task_id_list": JobTask.objects.filter(
                status__in=[StatusType.RUNNING, StatusType.QUEUE],
                host__bk_biz_id=bk_biz_id,
                host__bk_cloud_id=bk_cloud_id
            ).values_list("id", flat=True)
        })

    def perform_destroy(self, instance):
        instance.destroy_task()

    @list_route(methods=["get"], url_path="(?P<job_id>\d+)/get_failed_hosts")
    def get_failed_hosts(self, request, bk_biz_id, job_id):

        job_tasks = JobTask.objects.filter(
            host__bk_biz_id=bk_biz_id,
            status__in=[StatusType.FAILED],
            job_id=job_id,
        )

        _data = []
        for job_task in job_tasks:
            _serializer = HostTaskResultSerializer(job_task)
            data = _serializer.data
            _data.append(data)

        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": _data
        })

    @detail_route(methods=["get"], url_path="get_steps")
    def get_steps(self, request, bk_biz_id, pk):
        self.bk_biz_id = bk_biz_id
        instance = self.get_object()
        job_type = instance.job_type
        job_steps = JOB_STEP_MAPPING.get(job_type)

        steps = []
        i = 0
        for j in job_steps:
            i += 1
            step = STEP_CHOICES[j]
            steps.append({
                "step": i,
                "name": step[0],
                "display": step[1]
            })

        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": steps
        })

    @list_route(methods=["post"], url_path="split_params")
    def split_params(self, request, bk_biz_id, *args, **kwargs):
        self.bk_biz_id = bk_biz_id

        data = request.data
        data["bk_biz_id"] = self.bk_biz_id
        data["creator"] = data.get("creator", "") or request.user.username

        _serializer = JobSplitSerializer(data=request.data)
        _serializer.is_valid(raise_exception=True)
        data = _serializer.data

        node_type = data.get("node_type")
        op_type = data.get("op_type")

        global_params = data.pop("global_params")

        hosts = data.pop("hosts")
        os_hosts = {}
        for _host in hosts:
            host = Host.objects.get(is_deleted=False, **_host)
            os_hosts.setdefault(host.os_type, []).append(host)

        params = []

        if node_type == ProcType.PLUGIN:
            plugin = global_params.pop("plugin")
            plugin_id = plugin.get("id")
            plugin_instance = GsePluginDesc.objects.get(id=plugin_id)

            if op_type in [OpType.UPDATE, OpType.UPGRADE]:
                package = global_params.pop("package")
                pkg_name = package.get("pkg_name")

                for os, hosts in os_hosts.iteritems():
                    plugin = plugin_instance
                    package = plugin_instance.get_package_by_os(os, pkg_name)
                    control = plugin_instance.get_control_by_os(os)

                    param = self.generate_params(data, hosts, plugin, global_params, control=control, package=package)
                    params.append(param)
            else:
                for os, hosts in os_hosts.iteritems():
                    plugin = plugin_instance
                    control = plugin_instance.get_control_by_os(os)

                    param = self.generate_params(data, hosts, plugin, global_params, control=control)
                    params.append(param)

        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": params
        })

    def generate_params(self, data, hosts, plugin, global_params, control=None, package=None):
        new_data = data.copy()
        new_data["hosts"] = [{
            "conn_ips": host.inner_ip
        } for host in hosts]

        global_params["plugin"] = GsePluginSerializer(instance=plugin).data
        if control:
            global_params["control"] = ProcessControlInfoSerializer(instance=control).data
        if package:
            global_params["package"] = ProcessPackageSerializer(instance=package).data

        new_data["global_params"] = copy.deepcopy(global_params)

        return new_data


class GatewayJobViewSet(JobViewSet):
    '''
    用于网关接口 取消权限验证
    '''
    permission_classes = ()


class HostViewSet(ModelViewSet):
    '''
    获取主机列表
    '''
    queryset = Host.objects.filter(
        is_deleted=False).order_by("job_status", "-id")
    serializer_class = HostSerializer
    request_serializer_class = HostReqDataSerializer
    http_method_names = ["get", "post"]
    bk_biz_id = None
    request_params = {}

    def get_queryset(self):
        order_by_list = self.request_params.get("order_by").split(
            ",") if self.request_params.get("order_by") else []
        order_by_list.append('job_status')
        field_names = tuple(order_by_list)
        self.queryset = self.queryset.order_by(*field_names)

        if "ignore_page" in self.request_params:
            self.pagination_class = None

        if "bk_set_id" in self.request_params:
            # 从CC获取信息
            biz = Business(bk_biz_id=self.bk_biz_id)
            self.request_params[
                "inner_ip__in"] = biz.get_set_or_module_host_ip(
                self.request_params["bk_set_id"],
                self.request_params.get("bk_module_id")
            )
        if self.request_params.get("keyword") is not None:
            keyword = self.request_params["keyword"]
            self.queryset = self.queryset.filter(
                Q(inner_ip__contains=keyword) | Q(node_type__contains=keyword))
        if "version" in self.request_params:
            if len(self.request_params.get("id__in", [])) == 0:
                # 表示没有符合的信息
                return []
        # 新增ip精确查询
        if self.request_params.get("ip") is not None:
            ip = self.request_params["ip"]
            ips = ip.split(",")
            # 多ip匹配
            self.queryset = self.queryset.filter(
                Q(inner_ip__in=ips) | Q(inner_ip__in=ips))
            # 模糊匹配
            # self.queryset = self.queryset.filter(
            #     Q(inner_ip__contains=ip) | Q(outer_ip__contains=ip))
            # 精确匹配
            # self.queryset = self.queryset.filter(
            #     Q(inner_ip=ip) | Q(outer_ip=ip))

        if "os_type" in self.request_params:
            os_type = self.request_params["os_type"]
            self.queryset = self.queryset.filter(os_type=os_type)

        _serializer = HostFilterSerializer(data=self.request_params)
        _serializer.is_valid(raise_exception=True)
        filter_conditions = _serializer.data
        filter_queryset = self.queryset.filter(
            bk_biz_id=self.bk_biz_id).filter(**filter_conditions)
        return filter_queryset

    def get_serializer(self, *args, **kwargs):
        kwargs.get("data", {}).update({"bk_biz_id": self.bk_biz_id})
        return super(HostViewSet, self).get_serializer(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        _serializer = self.request_serializer_class(data=request.GET)
        _serializer.is_valid(raise_exception=True)
        self.request_params = _serializer.data
        return super(HostViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        return super(HostViewSet, self).retrieve(request, *args, **kwargs)

    @list_route(methods=['post'], url_path='check')
    def check_hosts_valid(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        hosts = request.data.get("hosts", [])
        validate_data = {
            "bk_cloud_id": request.data.get("bk_cloud_id", '0'),
            "bk_supplier_id": Business(bk_biz_id=self.bk_biz_id).bk_supplier_id
        }

        hosts = self.queryset.filter(
            bk_biz_id=self.bk_biz_id, inner_ip__in=hosts)
        validator = BulkHostValidator(hosts)
        validator(validate_data)
        return Response()

    @list_route(methods=['post'], url_path='proxy/check')
    def check_proxy_existed(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        bk_cloud_id = request.data.get("bk_cloud_id", [])
        proxys = self.queryset.filter(
            bk_cloud_id=bk_cloud_id,
            bk_biz_id=self.bk_biz_id,
            node_type='PROXY'
        )
        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": {
                "total": proxys.count(),
                "valid_count": proxys.filter(agent_status=1).count()
            }
        })


class HostLogViewSet(ModelViewSet):
    '''
    获取机器最后一次安装任务的日志和状态信息
    '''
    queryset = JobTask.objects.all()
    serializer_class = HostJobLogSerializer
    bk_biz_id = None
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):
        self.bk_biz_id = kwargs.get("bk_biz_id")
        return super(HostLogViewSet, self).retrieve(request, *args, **kwargs)

    def get_object(self):
        # 日志范围仅限Agent操作部分，过滤掉插件部分的任务
        objects = JobTask.objects.filter(
            host__id=self.kwargs["pk"],
            host__bk_biz_id=self.bk_biz_id).exclude(
            Q(job__job_type=JobType.UPDATE_AUTHINFO) |
            # Q(job__job_type=JobType.UPGRADE_CONFIG) |
            Q(job__job_type__endswith='_PLUGIN') |
            Q(job__job_type__startswith='IMPORT_')).order_by("-id")
        if objects:
            return objects[0]
        else:
            raise Http404(u"不存在任何日志信息")


class HostStatusViewSet(ModelViewSet):
    '''
    获取agent运行状态和版本信息
    '''
    queryset = HostStatus.objects.all()
    serializer_class = HostStatusSerializer
    request_serializer_class = HostStatusReqSerializer
    host_ids = []
    paginator = None

    query_params = {}

    def get_queryset(self):
        self.queryset = self.queryset.filter(**self.query_params)
        return self.queryset.filter(host__id__in=self.host_ids)

    def list(self, request, *args, **kwargs):
        self.host_ids = [item for item in request.GET.get(
            "host_ids", "").split(",") if item]
        self.bk_biz_id = kwargs.get("bk_biz_id")

        _serializer = self.request_serializer_class(data=request.GET)
        _serializer.is_valid(raise_exception=True)
        self.query_params = _serializer.data

        return super(HostStatusViewSet, self).list(request, *args, **kwargs)

    @list_route(methods=['get'], url_path='get_versions')
    def get_versions(self, request, bk_biz_id):
        self.bk_biz_id = bk_biz_id

        _serializer = self.request_serializer_class(data=request.GET)
        _serializer.is_valid(raise_exception=True)
        filter_conditions = _serializer.data

        queryset = self.queryset.filter(
            host__bk_biz_id=bk_biz_id
        ).filter(
            **filter_conditions
        ).values_list("version").annotate(count=Count("id"))

        data = [dict(
            version=version,
            count=count
        ) for (version, count) in queryset]

        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": data
        })

    @list_route(methods=['get'], url_path='get_plugin_status')
    def get_plugin_status(self, request, bk_biz_id):
        self.bk_biz_id = bk_biz_id

        inner_ip = request.GET.get("ip", "")
        plugin = request.GET.get("plugin", "")

        host = Host.objects.get(bk_biz_id=bk_biz_id, inner_ip=inner_ip, is_deleted=False)
        bk_supplier_id = Business(bk_biz_id=bk_biz_id).bk_supplier_id

        _host = {
            "ip": host.inner_ip,
            "bk_supplier_id": int(bk_supplier_id),
            "bk_cloud_id": int(host.bk_cloud_id)
        }
        _key = "%s:%s:%s" % (host.inner_ip, bk_supplier_id, host.bk_cloud_id)
        agent = GSEAgent()
        data = agent.get_proc_status([_host], plugin)
        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": data
        })

    @list_route(methods=['get'], url_path='get_host')
    def get_host(self, request, bk_biz_id):
        self.bk_biz_id = bk_biz_id

        _serializer = HostStatusFilterSerializer(data=request.GET)
        _serializer.is_valid(raise_exception=True)
        filter_conditions = _serializer.data

        queryset = self.queryset.exclude(
            status="UNREGISTER").filter(**filter_conditions)
        data = []
        for row in queryset:
            _row = HostStatusFilterSerializer(instance=row)
            data.append(_row.data)

        return Response({
            "result": True,
            "code": ResponseCodeStatus.OK,
            "message": u'success',
            "data": data
        })


class GatewayHostStatusViewSet(HostStatusViewSet):
    '''
    用于网关接口 取消权限验证
    '''
    permission_classes = ()


class GsePluginViewSet(ModelViewSet):
    '''
    获取agent运行状态和版本信息
    '''
    queryset = GsePluginDesc.objects.all().order_by("-id")
    serializer_class = GsePluginSerializer
    paginator = None
    http_method_names = ["get", "post"]

    lookup_value_regex = '\w+'
    lookup_field = 'name'

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category is not None:
            self.queryset = self.queryset.filter(category=category)
        return self.queryset


class ProcessPackageViewSet(ModelViewSet):
    queryset = Packages.objects.all().filter(
        cpu_arch='x86_64'
    ).order_by("-id")
    serializer_class = ProcessPackageSerializer
    paginator = None
    http_method_names = ["get", "post"]

    def get_queryset(self):
        project = self.kwargs.get('process')
        os = self.request.GET.get("os", "linux").lower()
        if project is not None:
            self.queryset = self.queryset.filter(project=project, os=os)
        return self.queryset


class ProcessControlInfoViewSet(ModelViewSet):
    queryset = ProcControl.objects.all().exclude(os='windows').order_by("-id")
    serializer_class = ProcessControlInfoSerializer
    paginator = None
    http_method_names = ["get", "post"]

    lookup_value_regex = '\w+'
    lookup_field = 'project'


class JobLogViewSet(ModelViewSet):
    '''
    获取机器最后一次安装任务的日志和状态信息
    '''
    queryset = TaskLog.objects.all().order_by("create_time")
    serializer_class = LogSerializer
    paginator = None
    http_method_names = ["get"]

    def get_queryset(self):
        job_id = self.kwargs.get('job_id')
        if job_id is not None:
            self.queryset = self.queryset.filter(job_id=job_id)
        return self.queryset

    @list_route(methods=["get"], url_path="get_steps")
    def get_steps(self, request, job_id):

        job = Job.objects.get(id=job_id)
        job_type = job.job_type
        job_steps = JOB_STEP_MAPPING.get(job_type)
        job_steps_count = len(job_steps)

        rows = self.queryset.filter(job_id=job_id, flag=FlagType.STEP)
        data = []

        for index, row in enumerate(rows):
            row = LogSerializer(instance=row)
            _d = row.data

            # 当前步骤前面的步骤肯定都是SUCCESS（因为我们不允许忽略中间错误）
            if index < len(rows) - 1:
                _d['status'] = "SUCCESS"
                data.append(_d)
                continue

            # 使用统计意义上的任务状态作为当前步骤的状态
            if job.job_status == "RUNNING":
                _d['status'] = "RUNNING"
            elif job.job_status == "SUCCESS":
                _d['status'] = "SUCCESS"
            elif job.job_status == "FAILED":
                _d['status'] = "FAILED"
            else:
                _d['status'] = "PARTIAL_SUCCESS"

            data.append(_d)

        return Response({
            "result": True,
            "data": data,
            "code": ResponseCodeStatus.OK,
            "message": "success"
        })

    @list_route(methods=["get"], url_path="get_step_log/(?P<log_id>\d+)")
    def get_step_log(self, request, *args, **kwargs):
        job_id = self.kwargs.get('job_id')
        self.queryset = self.queryset.filter(job_id=job_id)

        log_id = self.kwargs.get('log_id')
        try:
            step_log = self.queryset.filter(flag=FlagType.STEP).get(id=log_id)
            next_step_logs = self.queryset.filter(
                flag=FlagType.STEP
            ).filter(id__gt=log_id)
            if next_step_logs:
                next_step_log = next_step_logs[0]
                rows = self.queryset.filter(
                    id__gt=log_id,
                    id__lt=next_step_log.id
                )
            else:
                rows = self.queryset.filter(id__gt=log_id)

            data = []
            for row in rows:
                row = LogSerializer(instance=row)
                data.append(row.data)

            return Response({
                "result": True,
                "data": data,
                "code": ResponseCodeStatus.OK,
                "message": "success"
            })
        except Exception, e:
            return Response({
                "result": False,
                "data": [],
                "code": ResponseCodeStatus.OBJECT_NOT_EXIST,
                "message": "查询对象不存在"
            })
