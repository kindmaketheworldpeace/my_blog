# -*- coding: utf-8 -*-
"""
    配置平台常规调用，拷贝修改自`数据平台`
"""

from django.core.cache import cache
from django.utils.translation import ugettext as _
import json

from common.log import logger
from .esbclient import client, client_v2, client_backend
from .exceptions import ComponentCallError, PlatDoesNotExistError
from node_man.constants import StatusType


class APIModel(object):
    """接口数据模型类"""

    KEYS = []

    @classmethod
    def init_by_data(cls, data):
        kvs = {_key: data[_key] for _key in cls.KEYS}
        o = cls(**kvs)
        o._data = data
        return o

    def __init__(self, *args, **kwargs):
        self._data = None

    def _get_data(self):
        """
        获取基本数据方法，用于给子类重载
        """
        raise NotImplementedError

    @property
    def data(self):
        """接口数据模型抽象"""
        if self._data is None:
            self._data = self._get_data()

        return self._data


class Business(APIModel):
    """
    从 CC 读取业务数据
    cache
        | -- cc_biz_list 缓存业务列表，过期时间 1 分钟
    """
    AUTH_ROLES = ['Maintainers']

    def __init__(self, bk_biz_id=None):
        super(Business, self).__init__()
        self.bk_biz_id = bk_biz_id

    def has_admin_auth(self, username):
        """
        用户是否有业务权限
        """
        try:
            admins = self.admins
            return username in self.admins
        except ComponentCallError:
            return False

    def _get_data(self):
        """TODO: 加缓存"""
        try:
            _data = client.cc.get_app_by_id({'app_id': self.bk_biz_id})
        except ComponentCallError as e:
            _data = []
            logger.warning(_(u"获取单个业务详情异常，args=%s") % (e.args,))

        return _data[0] if len(_data) > 0 else None

    @property
    def bk_biz_name(self):
        if self.data is None:
            return _(u"未知业务")
        return self.data['ApplicationName']

    @property
    def bk_supplier_id(self):
        if self.data is None:
            return 0
        if self.data.get('CompanyID'):
            return self.data["CompanyID"]
        return 0

    @property
    def admins(self):
        """
        业务负责人，可以自定义增删业务角色
        """
        if self.data is None:
            return []
        admins = []
        for _role in self.AUTH_ROLES:
            admins.extend(self.data[_role].split(';'))
        return admins

    @property
    def level(self):
        """
        获取业务拓扑级别
        """
        return int(self.data['Level'])

    @staticmethod
    def add_plat_id(plat_name):
        """
        新增云区域
        """
        return client_backend.cc.add_plat_id({
            'plat_name': plat_name
        })

    @staticmethod
    def delete_plat(plat_id):
        """
        删除云区域
        """
        return client.cc.del_plat({
            'plat_id': plat_id
        })

    @staticmethod
    def get_plat_id(plat_name):
        plats = client_backend.cc.get_plat_id()
        for item in plats:
            if plat_name == item["platName"]:
                return item["platId"]
        raise PlatDoesNotExistError

    @staticmethod
    def rename_plat(plat_id, plat_name):
        client_v2.cc.update_inst(bk_obj_id="plat",
                                 bk_inst_id=plat_id,
                                 bk_cloud_name=plat_name
                                 )

    @classmethod
    def get_or_create_plat_id(cls, plat_name):
        try:
            return cls.get_plat_id(plat_name)
        except PlatDoesNotExistError:
            return cls.add_plat_id(plat_name)

    @staticmethod
    def get_all_plat():
        return client.cc.get_plat_id()

    @classmethod
    def get_app_by_user(cls, user, id_only=False):
        """
        获取用户有权限的业务列表
        [{
            "ApplicationID": "1",
            "ApplicationName": "资源池",
            "CompanyID": "0",
        }]
        """
        # supplier_account = client_v2.bk_login.get_user().get("bk_supplier_account", "0")
        # supplier_account = getattr(user, "bk_supplier_account", "")
        # data = client.cc.get_app_by_user(bk_supplier_account=supplier_account)
        data = client.cc.get_app_by_user()
        return map(lambda _d: {
            'ApplicationID': _d['ApplicationID'],
            'ApplicationName': _d['ApplicationName'],
            'CompanyID': _d['CompanyID']
        }, data)

    @classmethod
    def get_app_by_user_role(cls, user, id_only=False):
        """
        获取用户有权限的业务列表
        """
        api_params = {
            'username': user,
            'user_role': ','.join(cls.AUTH_ROLES)
        }
        data = client.cc.get_app_by_user_role(api_params)

        ret = []
        for _role in cls.AUTH_ROLES:
            if _role in data:
                ret.extend(data[_role])

        if id_only:
            return [int(_d['ApplicationID']) for _d in ret]

        return ret

    @classmethod
    def get_appid_by_host(cls, host, bk_cloud_id, bk_supplier_id):
        # 根据主机拉取对应的业务信息
        hosts = cls.search_hosts_info([host], bk_cloud_id, bk_supplier_id).get("info")
        for host_data in hosts:
            if host_data["biz"]["default"] != 1:
                # 如果是业务资源池的，就忽略
                return host_data["biz"]
        return None

    def get_agent_status(self, hosts):
        """
        查询主机 Agent 状态
        """
        api_params = {
            'app_id': self.bk_biz_id,
            'ip_infos': hosts,
            'is_real_time': 1
        }
        return client.job.get_agent_status(api_params)

    def get_set_module_tree(self, add_hosts=0):
        """
        查询业务下的所有大区和模块拓扑信息
        [{
            "SetID": "4",
            "Children": [
                {
                    "ModuleName": "空闲机",
                    "ModuleID": "5"
                },
                {
                    "ModuleName": "故障机",
                    "ModuleID": "6"
                }
            ],
            "SetName": "空闲机池"
        },
        {
            "SetID": "5",
            "Children": [
                {
                    "ModuleName": "job",
                    "ModuleID": "7"
                }
            ],
            "SetName": "作业平台"
        }]
        """

        def _clean_topo_tree(topo_data, module_hosts):

            sets = []

            def _clean_modules(modules):
                return [{
                    'HOSTS': module_hosts.get(str(_m['bk_inst_id']), []),
                    'ModuleID': _m['bk_inst_id'],
                    'ModuleName': _m['bk_inst_name']
                } for _m in modules]

            def _clean_topo_tree_except_internal_module(sets, topo_data):
                """
                简化 CC 返回的 TOPO 结构
                """
                for obj in topo_data:
                    if obj['bk_obj_id'] == 'set':
                        sets.append({
                            'SetID': obj['bk_inst_id'],
                            'SetName': obj['bk_inst_name'],
                            'Children': _clean_modules(obj['child'])
                        })
                        continue

                    # 递归
                    _clean_topo_tree_except_internal_module(sets, obj['child'])

            # 获取业务空闲机和故障机模块
            internal_module = client_v2.cc.get_biz_internal_module(api_params)

            sets.append({
                'SetID': internal_module['bk_set_id'],
                'SetName': internal_module['bk_set_name'],
                'Children': [{
                    'HOSTS': module_hosts.get(str(_m['bk_module_id']), []),
                    'ModuleID': _m['bk_module_id'],
                    'ModuleName': _m['bk_module_name']
                } for _m in internal_module['module']]
            })

            _clean_topo_tree_except_internal_module(sets, topo_data)

            return sets

        api_params = {
            'bk_biz_id': self.bk_biz_id
        }

        data = client_v2.cc.search_biz_inst_topo(api_params)

        _module_hosts = self.get_app_host_list(group_by='module') if add_hosts else {}

        return _clean_topo_tree(data, _module_hosts)

    def get_app_host_list(self, group_by=None):
        """
        查询业务下的主机列表
        """
        api_params = {
            'app_id': self.bk_biz_id,
        }
        try:
            hosts = client.cc.get_app_host_list(api_params)
        except ComponentCallError as e:
            logger.warning(_(u"获取主机列表异常，error=%s") % e.message)
            hosts = []

        # 分组返回
        _module_hosts = {}
        if group_by == 'module':
            for h in hosts:
                module_id = h['ModuleID']
                if module_id in _module_hosts:
                    _module_hosts[module_id].append(h['InnerIP'])
                else:
                    _module_hosts[module_id] = [h['InnerIP']]
            return _module_hosts

        return hosts

    def get_set_module_hosts(self, set_id):
        """
        查询业务大区下的的主机列表
        """
        api_params = {
            'app_id': self.bk_biz_id,
            'set_id': set_id
        }
        try:
            hosts = client.cc.get_set_host_list(api_params)
        except ComponentCallError as e:
            logger.warning(_(u"获取主机列表异常，error=%s") % e.message)
            hosts = []

        modules = []
        cleaned_host = {}
        for host in hosts:
            # 统计各模块主机数量
            module_name = host['ModuleName']
            module_id = host['ModuleID']
            module_names = [_m['ModuleID'] for _m in modules]
            if module_name not in module_names:
                modules.append({'ModuleName': module_name, 'ModuleID': module_id})
            host_num = cleaned_host.get(module_name, 0)
            cleaned_host.update({
                module_name: host_num + 1
            })
        for _m in modules:
            _m.update({'HOST_NUM': cleaned_host[_m['ModuleName']]})

        return sorted(modules, key=lambda _d: _d['HOST_NUM'], reverse=True)

    def get_module_hosts(self, module_id, add_agent_status=False):
        """
        查询业务模块的主机列表
        @param module_id {int} 模块ID
        @param add_agent_status {boolean} 是否添加 Agent 状态
        """
        api_params = {
            'app_id': self.bk_biz_id,
            'module_id': module_id
        }
        try:
            hosts = client.cc.get_module_host_list(api_params)
        except ComponentCallError as e:
            logger.warning(_(u"获取主机列表异常，error=%s") % e.message)
            hosts = []
        cleaned_hosts = [
            {'plat_id': _h['Source'], 'ip': _h['InnerIP']} for _h in hosts
        ]

        if add_agent_status and len(hosts) > 0:
            status = self.get_agent_status(cleaned_hosts)
            m_status = {
                '%s:%s' % (_s['plat_id'], _s['ip']): _s['status']
                for _s in status
            }
            for _h in cleaned_hosts:
                _key = '%s:%s' % (_h['plat_id'], _h['ip'])
                if _key in m_status:
                    if m_status[_key] == 1:
                        _h['status'] = 1
                        _h['status_display'] = _(u"Agent正常")
                    else:
                        _h['status'] = 0
                        _h['status_display'] = _(u"Agent异常")
                else:
                    _h['status'] = -1
                    _h['status_display'] = _(u"检测不到Agent")

        return cleaned_hosts

    def get_set_or_module_host_ip(self, set_id, module_id=None):
        """
        查询业务大区下的的主机列表
        """
        hosts = self.get_app_host_list()
        host_ips = []
        for host in hosts:
            if module_id is None:
                if str(host["SetID"]) == set_id:
                    host_ips.append(host["InnerIP"])
            elif str(host["ModuleID"]) == module_id:
                host_ips.append(host["InnerIP"])
        return host_ips

    @staticmethod
    def search_hosts_info(hosts, bk_cloud_id, bk_supplier_id):
        params = {
            "ip": {
                "data": hosts,
                "exact": 1,
                "flag": "bk_host_innerip"
            },
            "condition": [

                {
                    "bk_obj_id": "biz",
                    "fields": ['bk_biz_id', 'bk_biz_name', 'default'],
                    "condition": [
                        {
                            "field": "bk_supplier_id",
                            "operator": "$eq",
                            "value": int(bk_supplier_id)
                        }
                    ]
                },
                {
                    "bk_obj_id": "host",
                    "fields": ['bk_cloud_id'],
                    "condition": [
                        {
                            "field": "bk_cloud_id",
                            "operator": "$eq",
                            "value": int(bk_cloud_id)
                        }
                    ]

                }

            ],
            "page": {
                "start": 0,
                "limit": 200,
            },
            "pattern": ""
        }
        return client_v2.cc.search_host(params)

    def add_host_to_resource(self, bk_cloud_id, bk_hosts, bk_supplier_id, import_from="3"):
        '''

        :param bk_cloud_id:
        :param bk_hosts: [inner_ip1,inner_ip2]
        :param import_from:
        :return:
        '''
        try:
            bk_cloud_id = int(bk_cloud_id)
        except:
            return False, u'bk_cloud_id必须是整形数据'
        if not isinstance(bk_hosts, list):
            return False, u'bk_hosts字段必须是数组类型'
        host_info = {str(index): {"bk_host_innerip": bk_host_innerip,
                                  "bk_cloud_id": int(bk_cloud_id),
                                  "import_from": import_from} for index, bk_host_innerip in
                     enumerate(bk_hosts)
                     }
        params = {"bk_supplier_id": int(bk_supplier_id) if bk_supplier_id else 0,
                  "host_info": host_info,
                  "bk_biz_id": self.bk_biz_id,
                  'ignore_error': True
                  }
        result = client_v2.cc.add_host_to_resource(params)
        if result is None:
            raise ComponentCallError(
                {"message": u"unknown component's error: the response is None",
                 "code": u"UNKNOWN ERROR"})
        # 以下是对CC的接口返回做各种判断
        for index in host_info:
            host_info[index]["result"] = {"status": StatusType.SUCCESS, "err_desc": "success"}
        for error in result.get("error") or []:
            if u'数据重复' in error:
                # CC接口返回数据没有标明错误码，所以按照错误提示来判断了
                continue
            index = error[0]
            if index in host_info:
                host_info[index]["result"] = {"status": StatusType.FAILED, "err_desc": error}
        return True, host_info.values()


class GSEAgentApiModel(APIModel):
    def __init__(self, bk_biz_id=None):
        super(GSEAgentApiModel, self).__init__()
        self.bk_biz_id = bk_biz_id

    @staticmethod
    def get_agent_status_and_info(params, **kwargs):
        '''

        :param params:
            "bk_supplier_id": 0,
            "hosts": [
                {
                    "ip": "10.0.0.1",
                    "bk_cloud_id": 0
                }
            ]

        :param kwargs:

        :return:

        {"bk_cloud_id:inner_ip":{}}

        {
            "0:10.0.0.1": {
                "ip": "10.0.0.1",
                "version": "V0.01R060D38",
                "bk_cloud_id": 0,
                "bk_agent_alive": 0|1,
                "parent_ip": "10.0.0.2",
                "parent_port": 50000
            }
        }
        '''
        logger.info(u"component::get_agent_status_and_info")
        status_data = client_v2.gse.get_agent_status(params)
        version_data = client_v2.gse.get_agent_info(params)
        for key, value in version_data.iteritems():
            status_data[key].update(value)
        return status_data
