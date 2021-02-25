# -*- coding: utf-8 -*-
"""
    gse相关接口测试：

        1. 进程控制
        2. 进程注册
        3. 进程查询
        4. 任务查询

"""
import json

import os

from copy import deepcopy

import time
from django.conf import settings
from django.test import TestCase
from django.utils import unittest

from blueking.component.client import ComponentClient
from node_man.tests.base_test import BaseTest


class GseTestCase(BaseTest):
    """测试类"""

    def setUp(self):
        """
        初始化数据
        """
        self.hosts = [
            {
                "ip": self.ip,
                "bk_cloud_id": self.bk_cloud_id,
                "bk_supplier_id": self.bk_supplier_id
            }
        ]
        self.operate_key = "{bk_cloud_id}:{bk_supplier_id}:{ip}:{namespace}".format(
            bk_cloud_id=self.bk_cloud_id,
            bk_supplier_id=self.bk_supplier_id,
            ip=self.ip,
            namespace=self.NAMESPACE
        )

        self.common_args = {
            "namespace": self.NAMESPACE,
            "meta": {
                "namespace": self.NAMESPACE,
                "name": self.proc_name,
                "labels": {
                    # TODO
                    # "source": "official",
                    "procname": self.proc_name
                }
            },
            "hosts": self.hosts
        }

        self.client = ComponentClient(
            app_code=settings.APP_ID,
            app_secret=settings.APP_TOKEN,
            common_args={'username': 'admin'},
        )
        self.client.set_bk_api_ver("v2")

    def create_spec_params(self, proc_name):
        return {
            "identity": {
                "proc_name": proc_name,
                "setup_path": self.setup_path,
                "pid_path": os.path.join(self.pid_path, proc_name),
                # "config_path": "",
                # "log_path": ""
            },
            "control": {
                "start_cmd": "./start.sh",
                "stop_cmd": "./stop.sh",
                "restart_cmd": "./restart.sh",
                "reload_cmd": "./reload.sh",
                "kill_cmd": "./kill.sh",
                "version_cmd": "./version.sh",
                "health_cmd": "./health.sh"
            },
            "resource": {
                "cpu": 10.0,
                "mem": 10.0,
                # "fd": 10000,
                # "disk": 100,
                # "net": 0
            },
            "monitor_policy": {
                "auto_type": 1,
                # "start_check_secs": 5,
                # "stop_check_secs": 5,
                # "start_retries": 3,
                # "start_interval": 20,
                # "crotab_rule": ""
            },
            # "warn_report_policy": {
            #     "report_id": 0
            # },
            # "configmap": [
            #     {
            #         "path": "",
            #         "md5": ""
            #     }
            # ]
        }

    @unittest.skip("always skip")
    def test_get_agent_status(self):

        url = self.get_agent_status_url

        kwargs = {
            "bk_supplier_id": 0,
            "hosts": self.hosts
        }
        res = self.client.gse.get_agent_status(**kwargs)
        print json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

    # @unittest.skip("always skip")
    def test_register_proc_info(self):
        """
        url: 接口url文档
        """
        url = self.register_proc_info_url

        kwargs = deepcopy(self.common_args)
        kwargs.update(**{
            "spec": self.create_spec_params(self.proc_name)
        })

        res = self.client.gse.register_proc_info(**kwargs)
        print url, json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

    # @unittest.skip("always skip")
    def test_get_proc_status(self):
        """
        url: 接口url文档
        """
        url = self.get_proc_status_url

        kwargs = self.common_args
        res = self.client.gse.get_proc_status(**kwargs)
        print url, json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

    # @unittest.skip("always skip")
    def test_operate_proc(self):

        url = self.operate_proc_url

        kwargs = deepcopy(self.common_args)
        kwargs.update(**{
            "op_type": 9
        })
        res = self.client.gse.operate_proc(**kwargs)
        print url, json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

    @unittest.skip("always skip")
    def test_get_proc_operate_result(self):
        """
        url = self.get_proc_operate_result_url
        {
            "result": true,
            "code": 0,
            "message":"success",
            "data":{
                "1:1:127.0.0.1:gse:proc-test": {
                  "errcode": 0,
                  "errmsg": "success",
                  "content": ""
                }
              }
            }
        }
        data中key为bk_cloud_id:bk_supplier_id:ip:namespace:name的组合，例如1:1:127.0.0.1:gse:proc-test，value为对应的结果；
        value为json格式，包含errcode、errmsg、content字段。其中errcode为0，表示成功；为115，表示处理中，需要重试；为其他非0字段表示失败；
        content字段无确切含义；
        """

        url = self.get_proc_operate_result_url
        kwargs = {
            "namespace": self.NAMESPACE,
            "task_id": self.task_id
        }
        res = self.client.gse.get_proc_operate_result(**kwargs)
        print url, json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

    def create_proc_operate_task(self, op_type):
        """进程操作"""

        OPERATE_DICT = {
            "START": 0,
            "STOP": 1,
            "CHECK": 2,
            "CONTROL": 3,
            "CANCEL_CONTROL": 4,
            "RESTART": 7,
            "RELOAD": 8,
            "KILL": 9,
        }

        # 启动basereport（自动托管）
        kwargs = deepcopy(self.common_args)
        kwargs.update(**{
            "op_type": OPERATE_DICT.get(op_type)
        })
        res = self.client.gse.operate_proc(**kwargs)
        print json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

        return res.get('data').get('taskid')

    def poll_operate_task(self, task_id):
        """轮询任务结果"""
        url = self.get_proc_operate_result_url

        kwargs = {
            "namespace": self.NAMESPACE,
            "task_id": task_id
        }
        res = self.client.gse.get_proc_operate_result(**kwargs)
        print url, json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

        key = ":".join([self.NAMESPACE, self.proc_name, self.bk_cloud_id, self.ip])
        err_code = json.loads(res.get('data').get(key)).get('errcode')
        # err_code = res.get('data').get(self.operate_key).get('errcode')


        # 轮询
        while err_code == 115:
            res = self.client.gse.get_proc_operate_result(**kwargs)
            print url, json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
            time.sleep(3)

            self.assertIs(res.get('result'), True)
            key = ":".join([self.NAMESPACE, self.proc_name, self.bk_cloud_id, self.ip])
            err_code = json.loads(res.get('data').get(key)).get('errcode')

        if err_code == 0:
            print "operate success"

    def ensure_proc_status(self, status):
        """状态确认"""

        url = self.get_proc_status_url
        kwargs = self.common_args
        res = self.client.gse.get_proc_status(**kwargs)
        print url, json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)
        self.assertIs(res.get('data').get('proc_infos')[0].get('status'), status)

    @unittest.skip("always skip")
    def test_add_basereport(self):
        """
        gse进程管理接口实现进程重启、启动等操作的限制有哪些（需要托管？对插件本身有什么要求？）
                更新： 停止进程 --》删除或者备份文件（执行脚本）--》下发文件到目标机器 --》 执行解压脚本 --》进程管理（启动）
                新增插件：
                注册进程信息 --》删除或者备份文件（执行脚本）--》下发文件到目标机器 --》 执行解压脚本 --》进程管理（启动） -> 查结果
                启动进程 实际上是 启动 + 托管进程

            注册basereport(gse)-> 备份文件(job) -> 下发文件(job) -> 解压文件(job) -> 进程管理(gse)
        """
        # 注册basereport
        kwargs = deepcopy(self.common_args)
        kwargs.update(**{
            "spec": self.create_spec_params("basereport")
        })
        res = self.client.gse.register_proc_info(**kwargs)
        print json.dumps(kwargs, indent=2), json.dumps(res, indent=2)
        self.assertIs(res.get('result'), True)

        print "backup file..."
        print "transport file..."
        print "start or restart plugin proc"

        # 启动basereport（自动托管）
        task_id = self.create_proc_operate_task("START")

        # 查询basereport启动结果
        print "check operate result"
        self.poll_operate_task(task_id)

        # 动态运行状态。0为未注册，1为运行中，2为停止
        self.ensure_proc_status(1)