# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import serializers, renderers
from rest_framework.decorators import list_route
from rest_framework.response import Response

from node_man.component.viewsets import GenericViewSet
from node_man.constants import JobType, ProcStateType, OsType
from node_man.models import KV, Job, Host, JobTask, TaskLog, HostStatus
from node_man.backend.scheduler import installer
from node_man.utils.simple_rsa import rsa_encrypt, rsa_decrypt


class TestViewSet(GenericViewSet):
    """
    后台任务测试相关接口
    """
    serializer_class = serializers.Serializer
    permission_classes = []

    def reset_db(self):
        """数据复位"""
        KV.objects.all().delete()
        HostStatus.objects.all().delete()
        Host.objects.all().delete()
        Job.objects.all().delete()
        JobTask.objects.all().delete()

        KV.objects.get_or_create(key='nginx', defaults={'v_json': {
            'inner_ip': ':80',
            'outer_ip': ':80'
        }})

    @list_route(methods=['get'], url_path='test_install_proxy')
    def test_install_proxy(self, request):
        """安装proxy测试
        http://dev.paas-dev.xxxx.com:8000/tests/test_install_proxy/?cloud=1&ip=ip&node_type=PROXY
        """
        inner_ip = request.query_params.get('inner_ip')
        password = request.query_params.get('password')
        bk_biz_id = request.query_params.get('bk_biz_id')
        bk_cloud_id = request.query_params.get('bk_cloud_id', 0)

        outer_ip = request.query_params.get('outer_ip', inner_ip)
        port = request.query_params.get('port', 22)
        has_cygwin = request.query_params.get('has_cygwin', True)
        job_type = request.query_params.get('job_type', JobType.INSTALL_PROXY)

        node_type = request.query_params.get('node_type', 'PROXY')
        auth_type = request.query_params.get('auth_type', 'PASSWORD')
        os_type = request.query_params.get('os_type', 'LINUX')
        account = request.query_params.get('account', 'root')

        proxy_list = [
            {
                'inner_ip': inner_ip,
                'outer_ip': outer_ip,
                'auth_type': auth_type,
                'node_type': node_type,
                'os_type': os_type,
                'account': account,
                'password': rsa_encrypt(password),
                'has_cygwin': has_cygwin,
                'port': port,
                'bk_biz_id': bk_biz_id,
                'bk_cloud_id': bk_cloud_id,
            }
        ]

        # 创建作业
        job = Job.objects.create(
            creator='admin',
            bk_biz_id=bk_biz_id,
            bk_cloud_id=bk_cloud_id,
            job_type=job_type,
        )

        # 创建主机
        for proxy in proxy_list:
            host = Host.objects.create(**proxy)
            JobTask.objects.create(job=job, host=host)
            HostStatus.objects.create(host=host)

        tsk = installer.apply_async(args=(job.pk,), kwargs={})

        return Response({'hosts': proxy_list, 'job_type': job_type})

    @list_route(methods=['get'], url_path='test_install_pagent')
    def test_install_pagent(self, request):
        """安装pagent测试"""
        host = Host.objects.create(**{
            'inner_ip': '',
            'outer_ip': '',
            'auth_type': 'PASSWORD',
            'node_type': 'PROXY',
            'os_type': 'linux',
            'account': 'root',
            'bk_biz_id': 3,
            'bk_cloud_id': 1,
        })
        HostStatus.objects.create(host=host, status=ProcStateType.RUNNING)

        # 创建作业
        job = Job.objects.create(
            creator='admin',
            bk_biz_id=3,
            bk_cloud_id=1,
            job_type=JobType.INSTALL_PAGENT,
        )

        pagent_list = [
            {
                'inner_ip': '',
                'outer_ip': '',
                'auth_type': 'PASSWORD',
                'node_type': 'PAGENT',
                'os_type': 'linux',
                'account': 'root',
                'password': 'nSNAW2Hs26cHCae4sdI1QnSUr8h6LUk3dh+E28APHipig6B8wQl'
                            'kah0QNjdOcP+W16I3rJLH0n+PQKmfan1Dyubetv6opt2yPbNm0z'
                            'pD7BIqjBwKKAJqc8ZE7s3508WgSKMag6tL5jdu4oEL5hR/5m43y'
                            'BSd6cuuOL7+FRQsHjM=',
                'has_cygwin': False,
                'port': 36000,
                'bk_biz_id': 3,
                'bk_cloud_id': 1,
            }
        ]

        # 创建主机
        for pagent in pagent_list:
            host = Host.objects.create(**pagent)
            JobTask.objects.create(job=job, host=host)

        tsk = installer.apply_async(args=(job.pk,), kwargs={})

        return Response({'job_id': job.pk, 'task_id': str(tsk.task_id)})

    @list_route(methods=['get'], url_path='test_uninstall_agent')
    def test_uninstall_agent(self, request):
        """卸载agent测试"""

        inner_ip = request.query_params.get('inner_ip')
        bk_biz_id = request.query_params.get('bk_biz_id')
        bk_cloud_id = request.query_params.get('bk_cloud_id', 0)

        host = Host.objects.get(inner_ip=inner_ip)

        # 创建作业
        job = Job.objects.create(
            creator='admin',
            bk_biz_id=bk_biz_id,
            bk_cloud_id=bk_cloud_id,
            job_type=JobType.UNINSTALL_AGENT,
        )

        # 创建主机
        JobTask.objects.create(job=job, host=host)
        tsk = installer.apply_async(args=(job.pk,), kwargs={'os_type': OsType.LINUX})
        return Response({'task_id': str(tsk.task_id)})

    @list_route(methods=['get'], url_path='test_celery_esb_client')
    def test_celery_esb_client(self, request):
        """celery中应用esbclient测试"""
        password = request.query_params.get('password')
        return Response({'password': rsa_decrypt(password)})

    @list_route(methods=['get'], url_path='test_get_task_log', renderer_classes=[renderers.StaticHTMLRenderer])
    def test_get_task_log(self, request):
        job_task = JobTask.objects.last()
        logs = TaskLog.objects.filter(
            (Q(job_id=job_task.job.pk) | Q(job_task_id=job_task.pk)) & Q(level__in=['user', 'error'])
        ).order_by('create_time')
        content = ''
        for log in logs:
            content += '<pre>{}</pre>'.format(log.content)
        return Response(content)
