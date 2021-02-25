# 接口文档
----

## 一、接口格式规范


### 1. `统一前缀`：`/api/`


### 2. `返回整体结构说明`：

```js
// 对象型 - object
{
	data: object（list）,
	message: 'success',
	code: 0,
	result:true
}
// 异常返回：
{
	result:false,
	data: object,
	message(s): ''
	code: 'error_code'
}

```

|参数|说明|
|-----|-----|
|result|请求是否正常，true :正确处理，false:异常处理|
|code|请求错误码，string类型，根据错误码判断message的类型|
|message|错误信息，string类型，code非VALIDATE_ERROR情况下使用|
|messages|错误信息列表，code为VALIDATE_ERROR的情况下使用，多位参数校验产生的问题|
|data|返回的数据，错误情况为None|

######code错误码说明

|错误码|备注|
|------|------|
|OK|正常情况|
|UNAUTHORIZED|未登录情况|
|METHOD_NOT_ALLOWED|不允许的方法|
|PERMISSION_DENIED|权限不够|
|SERVER_500_ERROR|服务器500错误|
|FORM_VALIDATE_ERROR|参数校验失败|
|REMOTE_CALL_ERROR|远程服务请求失败|
|COMPONENT_CALL_ERROR|组件调用异常|	
|FATAL_ERROR|未知异常|
|OBJECT_NOT_EXIST|请求对象不存在|
|NGINX_SETTING_ERROR|需要ngnix配置信息|




### 变量说明：url中{ var } 表示变量

其中：`bk_biz_id` 为业务ID ApplicationID

`job_id` 为host列表中对应的任务id

`host_id` 为host的id






## 二、主要接口

### 1. NGINX配置查询接口

~~url: /config/nginx/~~

url: /config/kv/?key=nginx

method: get


#####返回参数

##### data : object

|参数|参数类型|参数说明|
| ------| ------| ------ |
|inner_ip|string| "ip:port,ip:port", 以逗号分隔|
|outer_ip|string| "ip:port,ip:port", 以逗号分隔|

### 1.1 安装任务超时配置查询接口

url: /config/kv/?key=timeout

method: get


#####返回参数

##### data : object

```
{
    "message": "success",
    "code": "OK",
    "data": {
        "timeout": "180"
    },
    "result": true
}
```

### 2. NGINX配置更新接口

~~url: /config/nginx/~~

url: /config/kv/

method: post

#####请求参数

|参数|参数类型|参数说明|
| ------| ------| ------ |
|key|string|变量名关键字，固定为：nginx|
|inner_ip|string| "ip:port,ip:port", 以逗号分隔|
|outer_ip|string| "ip:port,ip:port", 以逗号分隔|

```
form: {
    'key': 'nginx',
	'inner_ip': 'ip:port, ip:port',
	'outer_ip': 'ip:port, ip:port'
}


```
### 2.1 安装任务超时配置更新接口

url: /config/kv/

method: post

#####请求参数

|参数|参数类型|参数说明|
| ------| ------| ------ |
|key|string|变量名关键字，固定为：timeout|
|inner_ip|string| "ip:port,ip:port", 以逗号分隔|
|outer_ip|string| "ip:port,ip:port", 以逗号分隔|
```
form: {
	'key': 'timeout',
	'timeout': 200
}


### 5. 查询主机列表接口
	- 根据大区和模块查找主机
	- 根据云区域过滤主机
	- 模糊查询

url: {bk_biz_id}/hosts/

method: get

#####请求参数

|参数|参数类型|是否必须|参数范围|
| ------| ------| ------ | ------ |
|bk_set_id|string| O |  |
|bk_module_id| string|O |  |
|bk_cloud_id| string|O |  |
|version| string|O | 默认全部,包含关系 |
|keyword| string|O |  |
|page_size| string|O |  默认10个一页 |
|page| string|O |当前页面，不带默认为1  |

#####返回结构

#####data：object

|参数|类型|参数说明|
| ------| ------ | ------ |
|page|int| 当前页面  |
|total_page|int| 总页面数 |
|count|int| 总数量  |
|next|string|下一页链接 |
|perevious|string| 上一页链接，没有为null |
|items|list| hosts集合 |

#####item 对象说明

|参数|类型|参数说明|
| ------| ------ | ------ |
|id|string| 唯一值  |
|inner_ip|string| 内网ip  |
|bk_cloud_id|string| 云区域id  |
|inner_ip|string| 内网ip  |
|node_type|string| 节点类型 |
|update_time|string| 更新时间|
|node_type|string| 节点类型 |
|status|dict| agent运行状态信息 |
|job_result| dict | 最后一次执行agent任务的执行日志和结果 |

#####status参数说明

|参数|类型|参数说明|
| ------| ------ | ------ |
|status| string |  当前状态（UNKNOWN，RUNNING，TERMINATED）|
|version| string |  版本信息|
|type| string | agent或plugin|
|name| string |进程的名称|


#####job_result参数说明

|参数|类型|参数说明|
| ------| ------ | ------ |
|status| string | 当前状态 ('QUEUE', 'RUNNING', 'SUCCESS', 'FAILED') |
|err_code| string | 任务结果 ，说明如下|
|step| string |任务步骤，说明如下|
|logs| string |任务日志|

```python
#任务状态码
CODE_TUPLE = (
    # 任务成功
    'INIT', #初始化
    'SUCCESS',# 成功
    'STILL_RUNNING',#运行中
    'CELERY_TASK_EXCEPT',#后台任务异常
    'CELERY_TASK_TIMEOUT',#后台任务超时
    'WAIT_AGENT_TIMEOUT',#
    'UNEXPECTED_RETURN',
    'CURL_FILE_FAILED',
    'REGISTER_FAILED',#注册失败
    'START_JOB_FAILED',#启动任务失败
    'JOB_TIMEOUT',#超时退出
    'IJOBS_FAILED',#ijobs作业失败
    'FORCE_STOP',# 强制终止
    'INSTALL_FAILED',#安装失败

    # SSH认证类错误
    'SSH_LOGIN_TIMEOUT', 'SSH_WRONG_PASSWORD',
    'SSH_LOGIN_EXCEPT', 'SSH_LOGIN_KEY_ERR',
    'NOT_SUPPORT_AUTH_WAY', 'SOCKET_TIMEOUT',

    # 其他错误
    'COMMAND_NOT_FOUND',
)

#步骤说明
STEP_CHOICES = [
    ('INIT', u'任务初始化'),
    ('SSH_LOGIN', u'登录目标主机'),
    ('INSTALL_DEP', u'安装基础依赖'),
    ('DOWNLOAD_FILE', u'下载安装包'),
    ('EXECUTE_SCRIPT', u'执行安装脚本'),
    ('SCRIPT_DONE', u'安装脚本执行完毕'),
    ('REGISTER_CMDB', u'注册主机到CMDB'),
    ('WAIT_AGENT', u'等待Agent连接就绪'),
    ('CREATE_JOB_SCRIPT', u'准备安装脚本'),
    ('EXECUTE_JOB', u'执行批量安装作业'),
    ('OVER_SUCCESS', u'安装成功'),
    ('OVER_FAILED', u'安装失败'),
]
```

```
param: {
	bk_set_id: "1",
	bk_module_id: "2",
	bk_cloud_id:"1",
	version:"1221"
	keyword: "sdfswerwrw",
	page_size:10}

response:
{
	"page": 1,
    "total_page": 1,
    "count": 10,
    "next": null,
    "previous": null,
    "items":[{
            "id": 12,
            "status": [
                {
                    "name": "gseagent",
                    "status": "UNKNOWN",
                    "version": "",
                    "logs":"abdsfwerwr",
                    "host_id": 12
                }
            ],
            "bk_biz_id": "1",
            "bk_cloud_id": "1",
            "inner_ip": "30.123.24.111",
            "outer_ip": null,
            "node_type": "AGENT",
            "os_type": "LINUX",
            "account": "test",
            "auth_type": "KEY",
            "password": "sfewrwrdxfesrw",
            "key": "asfw",
            "job_result": {
                "job_id": "14",
                "status": "QUEUE",
                "code": "",
                "step": "INIT"
            }
        }]
```
### 6. 查询主机Agent状态接口

url: /{bk_biz_id}/host_status/?host_ids=1
method: get

#####请求参数

|参数|参数类型|是否必须|参数范围|
| ------| ------| ------ | ------ |
|host_ids|string| M | 主机id，以逗号分隔 |

#####返回data参数说明

data:list
#####data内部元素参数说明

|参数|类型|参数说明|
| ------| ------ | ------ |
|status| string |  |
|version| string |  |
|type| string | agent或plugin|
|name| string |进程的名称|
|host_id| string |对应的host的id|
```
param: {
	host_ids: M, 主机ID， 以","分隔
}
item: [{
	 "name": "gse-agent",
     "status": "loading",
     "type": "agent",
     "version": "1.0.1",
     "host_id": 1
}]
```
### 7. 添加云区域接口

url: /{bk_biz_id}/clouds/
method: post

|参数|类型|说明|
|------|------|------|
|bk_cloud_name|string|云区域名称|

```
form: {
	bk_cloud_name: 云区域名称
}
```
### 8. 查询云区域列表接口

url: /{bk_biz_id}/clouds/
method: get

#####data:list

`返回参数说明`

|参数|类型|参数说明|
| ------| ------ | ------ |
|bk_cloud_id| string | id |
|bk_cloud_name| string | 名称 |

```
item: {
	bk_cloud_id: 1,
	bk_cloud_name: 2
}
```


### 9. 新增并安装、重装，卸载，移除任务类接口

url: {bk_biz_id}/tasks/

method: post

#####请求参数

|参数|参数类型|是否必须|参数范围|
| ------| ------| ------ | ------ |
|op_type|string| M | (INSTALL：安装,REINSTALL：重装,UNINSTALL：卸载,REMOVE:移除，UPDATE_AUTHINFO：保存)|
|node_type| string|M(卸载非必须) | (AGENT,PAGENT,PROXY) |
|bk_cloud_id| string|M |  |
|hosts| list|M |  |

#####host参数说明

|参数|参数类型|是否必须|参数范围|
| ------| ------| ------ | ------ |
|inner_ips|string| M | 内网ip列表，以逗号分隔|
|outer_ip| string|O(PROXY为 M) | PROXY必须|
|account| string|O |  |
|port| int|O |  |
|auth_type| string|O | KEY, PASSWORD, 默认PASSWORD |
|has_cygwin| bool|O | 默认false |
|password| string|O |  |
|key| string|O |  |



#####异常返回`messages`结构说明

>一般都有对应的字段，如inner_ip,outer_ip等，对号入座就可以


#####特殊字段说明：
|返回字段|字段类型|备注|
| ------| ------| ------ |
|non_field_errors|list| 针对非单个字段的校验错误 |
|host:{inner_ip}|list| 这里的inner_ip是前端传过来的内容，根据填写的ip对号入座 |



```python
{
    "messages": {
        "hosts": [
            {
                "host:10.110.140.131er": {
                    "inner_ip": [
                        "请输入一个有效的IPv4或IPv6地址。"
                    ]
                }
            }
        ],
         "non_field_errors":["这是一个不针对单个字段校验的问题"]
    },
    "code": "VALIDATE_ERROR",
    "data": null,
    "result": false
}
```


```
form:
	{  "hosts": [
            {
                    "inner_ips": "", #内网ip列表，以逗号分隔
                    "outer_ip": "",#外网ip
                    "account": "root",#帐号
                    "port": 22,#SSH端口
                    "auth_type": "KEY",#鉴权类型
                    "os_type":"LINUX",#系统类型
                    "password": "wadsfs",#密码
					"has_cygwin":false,#是否有xxxx
                    "key": "asfw"#密钥
            }
        ],
        "bk_cloud_id": "1",#云区域id
        "node_type": "AGENT",#节点类型
		"op_type":"INSTALL" #操作方法
    }


```


### 10.终止单个任务接口

url: {bk_biz_id}/tasks/{job_id}/

method: delete

result: ` true | false`


### 11.批量任务终止接口
url: {bk_biz_id}/tasks/bulk/?jobs=1,2,3
method: delete


###12. 日志查询接口

url: {bk_biz_id}/logs/{host_id}/

method: get

##### data:object
`返回数据data结构说明`

|参数|类型|参数说明|
| ------| ------ | ------ |
|status| string | 当前状态 |
|err_code| string | 任务结果 |
|step| string |任务步骤|
|logs| string |任务日志|

```
返回：
{"status": "XXXXx",
 "step": "XXXXX",
 "logs": "this is a tes \\r\\n",
 "err_code": "XXXXX"
}

```


##### 13.检测机器是否已安装

`url: {bk_biz_id}/hosts/check/`

method: post


#####请求参数说明

|参数|参数类型|是否必须|参数范围|
| ------| ------| ------ | ------ |
|hosts|list| M | ["127.0.0.1"]|
|bk_cloud_id|string| M | 云区域id|


`请求参数`


```
{
"bk_cloud_id":"0",
"hosts":["127.0.0.1"]
}
```


`返回结构`

```
{
    "messages": [{
       "10.208.56.19": "10.208.56.19:当前机器属于未知云区域",
        "10.208.56.16":"10.208.56.16:当前机器已经安装了agent"
    }],
    "code": "VALIDATE_ERROR",
    "data": null,
    "result": false
}
```



##### 13.检测机器是否已安装proxy

`url: {bk_biz_id}/hosts/proxy/check/`

method: post


#####请求参数说明

|参数|参数类型|是否必须|参数范围|
| ------| ------| ------ | ------ |
|bk_cloud_id|string| M | 云区域id|






`请求参数`


```
{
"bk_cloud_id":"0",
}
```


`返回参数data`

|参数|参数类型|参数范围|
| ------| ------| ------ |
|total|int|  当前proxy的总数|
|valid_count|int|  当前可用proxy的总数|



```
{
    "message": "success",
    "code": "OK",
    "data": {
        "valid_count": 0,
        "total": 0
    },
    "result": true
}
```


## 二、配置平台相关接口

### 1. 查询业务列表接口

`url: /cmdb/applications/`

method: get
##### data:object
`返回数据data结构说明`

|参数|类型|参数说明|
| ------| ------ | ------ |
|ApplicationName| string | 业务名称 |
|ApplicationID| string | 业务ID |
|CompanyID| string |公司ID|
```
[{
    "ApplicationName": "资源池", // 业务名称
    "ApplicationID": "1", // 业务ID
    "CompanyID": "0" // 开发商ID
}]
```


### 2. 查询大区和模块及主机拓扑

`url: /cmdb/{bk_biz_id}/topo/`

method: get


#####请求参数说明

|参数|参数类型|是否必须|参数范围|
| ------| ------| ------ | ------ |
|add_hosts|bool| O | 默认false,指定true的时候会返回模块下的主机列表|


`返回参数说明`


|参数|参数类型|备注|
| ------| ------| ------ |
|SetID|string| 大区id|
|Children|list| 模块集合|


|参数|参数类型|备注|
| ------| ------| ------ |
|Children.ModuleName|string| 模块名称|
|Children.ModuleID|string| 模块ID|
|Children.HOSTS|list 机器列表 ip列表（string）|

```
param: {
	add_hosts: 1 // 可选，指定add_host时会返回模块下的主机列表
}
item: {
            "SetID": "4",
            "Children": [
                {
                    "ModuleName": "空闲机",
                    "HOSTS": [
                        "1.1.1.1"
                    ],
                    "ModuleID": "5"
                },
                {
                    "ModuleName": "故障机",
                    "HOSTS": [
                        "192.168.0.3",
                        "192.168.0.4"
                    ],
                    "ModuleID": "6"
                }
            ],
            "SetName": "空闲机池"
 }
```

