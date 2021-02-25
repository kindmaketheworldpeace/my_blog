# -*- coding: utf-8 -*-
"""
    配置平台常规调用，拷贝修改自`数据平台`
"""

from django.core.cache import cache
from django.utils.translation import ugettext as _
import json

import settings
from blueking.component.client import ComponentClient
from common.log import logger
from .esbclient import client, client_v2
from .exceptions import ComponentCallError, PlatDoesNotExistError
from node_man.constants import StatusType



class GSEAgent(object):
    def __init__(self):
        super(GSEAgent, self).__init__()
        self.NAMESPACE = "nodeman"
        self.client = ComponentClient(
            app_code=settings.APP_ID,
            app_secret=settings.APP_TOKEN,
            common_args={'username': 'admin'},
        )
        self.client.set_bk_api_ver("v2")

    def get_proc_status(self, hosts, proc_name):
        '''
        获取进程状态
        :param params:
            "namespace": self.NAMESPACE,
            "meta": {
                "namespace": self.NAMESPACE,
                "name": proc_name,
                "labels": {
                    "procname": proc_name
                }
            },
            "hosts": [
                {
                    "ip": "127.0.0.1",
                    "bk_supplier_id": 0,
                    "bk_cloud_id": 0
                }
            ]

        :param kwargs:

        :return:

        '''

        kwargs = {
            "namespace": self.NAMESPACE,
            "meta": {
                "namespace": self.NAMESPACE,
                "name": proc_name,
                "labels": {
                    "procname": proc_name
                }
            },
            "hosts": hosts
        }
        result =  self.client.gse.get_proc_status(**kwargs)

        data = result.get("data", {}).get("proc_infos", [])


        return data



