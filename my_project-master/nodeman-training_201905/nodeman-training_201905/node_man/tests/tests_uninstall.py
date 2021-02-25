# -*- coding: utf-8 -*-

import sys

import time
from django.test import TestCase

from node_man.constants import JobType, ProcStateType, OsType
from node_man.models import Host, Job, JobTask, TaskLog, HostStatus, KV
from node_man.backend.scheduler import installer
from node_man.tests.base_test import BaseTest


class InstallProxyTest(BaseTest):
    """proxy安装任务测试流程"""
    def setUp(self):
        print sys._getframe().f_code.co_name

        KV.objects.create(key='nginx', v_json=self.v_json)

        host = Host.objects.create(**self.host)

        HostStatus.objects.create(host=host, status=ProcStateType.RUNNING)

        # 创建作业
        self.job = Job.objects.create(
            creator='admin',
            bk_biz_id=1,
            bk_cloud_id=1,
            job_type=JobType.UNINSTALL_AGENT,
        )

        # 创建主机
        JobTask.objects.create(job=self.job, host=host)

    def tearDown(self):
        print sys._getframe().f_code.co_name

    @classmethod
    def tearDownClass(cls):
        print sys._getframe().f_code.co_name

    def test_install_proxy(self):
        print sys._getframe().f_code.co_name
        installer.apply_async(args=(self.job.pk,), kwargs={'os_type': OsType.LINUX})
