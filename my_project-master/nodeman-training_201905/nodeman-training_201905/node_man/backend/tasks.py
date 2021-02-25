# -*- coding: utf-8 -*-
"""
原子任务
"""
import sys
import json
import time
import base64
import socket
import traceback

from billiard import SoftTimeLimitExceeded
from celery.task import task

from conf.default import RUN_VER
from node_man.component.esbclient import client, client_v2, client_backend
from node_man.component.exceptions import (ComponentCallError, NginxSettingError, NginxConnectionError)
from node_man.constants import (StatusType, TASK_TIMEOUT,
                                CodeType, OsType, StepType)
from node_man.backend.tools import (create_script_param, get_script_content,
                                    create_pagent_install_script)  # install_proxy_by_wmiexec,
# install_proxy_by_ssh,
#   install_aix_agent_by_ssh)

from node_man.backend.installers.windows_installer import WindowsInstaller
from node_man.backend.installers.linux_installer import LinuxInstaller
from node_man.backend.installers.aix_installer import AixInstaller
from node_man.backend.installers.installer import Installer
from node_man.models import Job, JobTask, HostStatus, Cloud, KV
from node_man import constants as const

# fix unicode error in some linux console
from node_man.utils.basic import now

try:
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass


# @task(soft_time_limit=TASK_TIMEOUT)
@task
def install_proxy(job_task_id, **kwargs):
    """
    安装proxy和直连agent
    """

    err_desc = ""
    job_task = JobTask.objects.get(pk=job_task_id)
    bk_supplier_account = job_task.job.bk_supplier_account
    for singleton in (client, client_v2, client_backend):
        singleton.set_bk_supplier_account(bk_supplier_account)
        singleton.set_username(job_task.job.creator)
    # 信号相关初始化
    job_task.update_status(StatusType.RUNNING)

    # 安装结果描述信息
    host, job = job_task.host, job_task.job
    try:
        # 区分系统类型安装
        if host.os_type == OsType.AIX:
            installer = AixInstaller(job_task)
        elif host.os_type == OsType.WINDOWS and host.has_cygwin is False:
            installer = WindowsInstaller(job_task)
        else:
            installer = LinuxInstaller(job_task)

        # TODO 可以这样使用Installer吗？
        # installer = Installer(job_task)

        err_code, err_desc = installer.execute()

        # 可以抽离为一个单独的流程：安装成功后的回调
        if err_code == CodeType.SUCCESS:

            # 回调1：注册主机到CMDB
            job_task.update_step(StepType.SCRIPT_DONE)

            # 录入配置平台
            is_registered, err_desc = job_task.job.register_host_to_cmdb(job_task)
            if is_registered:
                err_code = CodeType.SUCCESS

                # 安装成功后轮询agent状态
                job_task.update_step(StepType.WAIT_AGENT)
                job_task.poll_agent_status(expected_status=1)
            else:
                err_code, err_desc = CodeType.REGISTER_FAILED, u'register to cmdb failed: %s' % err_desc

    except NginxSettingError as error:
        job.log(u'error：%s' % error.message, 'user')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)
        err_code = CodeType.CELERY_TASK_EXCEPT

    except NginxConnectionError as error:
        job.log(u'error：%s' % error.message, 'user')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)
        err_code = CodeType.CELERY_TASK_EXCEPT

    # 任务超时，ssh读取超时
    except socket.timeout:
        err_desc = u"Socket timeout, install failed. Please check Log in Developer Center."
        job_task.log(err_desc, 'error')
        job_task.log(u'System error: %s' % traceback.format_exc(), 'error')
        err_code = CodeType.SOCKET_TIMEOUT

    # 任务超时，脚本执行超时
    except SoftTimeLimitExceeded:
        err_desc = u"Install script running time out(%ss), install failed." % KV.get_timeout_config()
        job_task.log(err_desc, 'error')
        err_code = CodeType.CELERY_TASK_TIMEOUT

    except Exception as err:
        err_desc = u'%s, please check Log in Developer Center.' % err
        job_task.log(u'System error: %s' % traceback.format_exc(), 'error')
        err_code = CodeType.CELERY_TASK_EXCEPT

    # 安装失败
    if err_code != CodeType.SUCCESS:
        job_task.update_status(StatusType.FAILED, err_code, err_desc)
        job_task.log(u'%s: %s' % (err_code, err_desc))
        return False

    # 回调2：托管插件到gse check-todo
    job.start_auto_launch_plugins()


@task
def install_pagent(job_id, **kwargs):
    """
    安装pagent
    """

    job = Job.objects.get(id=job_id)
    bk_supplier_account = job.bk_supplier_account
    for singleton in (client, client_v2, client_backend):
        singleton.set_bk_supplier_account(bk_supplier_account)
        singleton.set_username(job.creator)

    # 生成脚本->创建作业->解析作业结果->录入CMDB
    try:
        # 随机取一台可用的Proxy，用于执行脚本
        proxy = HostStatus.get_random_alived_proxy(job.bk_biz_id, job.bk_cloud_id)
        proxy_list = HostStatus.get_alived_proxy(job.bk_biz_id, job.bk_cloud_id, dict_format=True)

        # 更新步骤
        job.update_status(StatusType.RUNNING, step=StepType.CREATE_JOB_SCRIPT)

        # 生成批量安装脚本和安装参数
        pagent_install_script = create_pagent_install_script(job_id, 'install_pagent_%s.sh' % job_id)
        script_param = create_script_param(job.bk_cloud_id, proxy_list, run_mode=0, mode='agent')
        job.log(u'create pagent install script parameter[%s]' % script_param)

        kwargs = {
            "app_id": proxy.bk_biz_id,
            "ip_list": [{'ip': proxy.inner_ip, 'source': proxy.bk_cloud_id}],
            'script_timeout': 3000,
            'script_param': script_param,
            "type": 1,
            "account": "root",
        }

        job.log(u'job parameter is：[\n%s\n]' % json.dumps(kwargs, indent=2))
        kwargs.update({"content": base64.b64encode(pagent_install_script)})

        try:
            data = client.job.fast_execute_script(kwargs)
        except ComponentCallError as e:
            e.record_transaction(job.log, 'user')
            job.log(u'start job failed: %s' % e.message, 'user')
            job.update_status(StatusType.FAILED, CodeType.START_JOB_FAILED, e.message)
            return False

        # 填充作业ID
        task_inst_id = data.get('taskInstanceId')
        job.update_bk_job_id(task_inst_id)
        job.log(u'start job success，begin poll job status')

        # 更新步骤
        job.update_job_step(StepType.EXECUTE_JOB)

        # 等待任务
        status, err_code, err_desc = job.poll_job_result(task_inst_id)
        if status != StatusType.SUCCESS:
            job.log(u'job execute failed，install failed.', 'error')
            job.update_status(StatusType.FAILED, err_code, err_desc)
            return False

        # 解析日志
        job_result = job.parse_job_result()
        job.log(u'parse job log(success when status=3)：%s' % json.dumps(job_result, indent=2))

        # 更新安装结果
        job.update_job_result(job_result.get('result'))

        if not job_result.get('success_list'):
            job.log(u'no success ip need register to cmdb')
            return False

        # 回调1：注册主机到CMDB
        success_list = job_result.get('success_list')
        is_registered, err_desc = job.register_host_to_cmdb()

        if not is_registered:
            # 注册不成功分为两种：部分不成功，不需要再次更新task的状态
            if err_desc != "Partially failed":
                job.log(u'register to cmdb failed(%s): %s' % (err_desc, success_list))
                job.update_status(StatusType.FAILED, CodeType.REGISTER_FAILED, err_desc)
            else:
                job.update_status(StatusType.FAILED, CodeType.REGISTER_FAILED, err_desc, update_task=False)
            return False

        success_filter_condition = {"host__inner_ip__in": [host["inner_ip"] for host in success_list]}
        job.update_status(StatusType.SUCCESS, CodeType.SUCCESS, filter_kwargs=success_filter_condition)
        job.end_time = now()
        job.save()

        # 回调2：托管插件到gse check-todo
        job.start_auto_launch_plugins()

    except NginxSettingError as error:
        job.log(u'error: %s' % error.message, 'user')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)

    except NginxConnectionError as error:
        job.log(u'error: %s' % error.message, 'user')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)

    except Exception as err:
        job.log("{}: {}, please check Log in Developer Center.".format(CodeType.CELERY_TASK_EXCEPT, str(err)))
        job.log(u'System error: %s' % traceback.format_exc(), 'error')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)


@task
def uninstall_agent(job_id, **kwargs):
    """
    卸载agent
    """

    os_type = kwargs.get('os_type')
    job = Job.objects.get(id=job_id)
    bk_supplier_account = job.bk_supplier_account
    for singleton in (client, client_v2, client_backend):
        singleton.set_bk_supplier_account(bk_supplier_account)
        singleton.set_username(job.creator)

    need_remove = kwargs.get('need_remove', False)

    # 生成脚本->创建作业->等待agent下线
    try:
        if need_remove:
            job.remove_hosts()
            job.update_status(StatusType.SUCCESS, CodeType.SUCCESS)
            return True

        # 更新步骤
        job.update_status(StatusType.RUNNING, step=StepType.CREATE_UNINSTALL_SCRIPT)

        # 区分系统类型下发作业
        if os_type == OsType.WINDOWS:
            accounts = ['Administrator', 'system']
            script_type_num = 2
        else:
            accounts = ['root']
            script_type_num = 1

        # TODO: account分批处理，仅获取正常状态的agent操作
        hosts = [{'ip': host.inner_ip,
                  'source': job.bk_cloud_id,
                  'node_type': host.node_type.lower()}
                 for host in job.get_job_hosts(filter_kwargs={"host__agent_status": 1})]
        task_inst_id = -1
        if hosts:
            # 获取远程卸载脚本
            nginx_type = 'inner_url'
            script_content = get_script_content(os_type, nginx_type=nginx_type)
            # 当有运行中的机器的时候，需要做卸载处理
            script_param = {"proxy": "-m proxy -r",
                            "agent": "-m client -r",
                            "pagent": "-m client -r"
                            }[hosts[0]['node_type']]
            for index, account in enumerate(accounts, 1):
                kwargs = {
                    "app_id": job.bk_biz_id,
                    "ip_list": hosts,
                    'script_timeout': 120,  # 2分钟
                    'script_param': script_param,
                    "type": script_type_num,
                    "account": account,

                }
                job.log(u'[%s]uninstall agent job parameter: %s' % (RUN_VER, kwargs), 'user')

                kwargs.update({"content": base64.b64encode(script_content.encode('utf-8'))})

                try:
                    data = client.job.fast_execute_script(**kwargs)
                except ComponentCallError as e:
                    if index != len(accounts):
                        # 试错机制，如果还没有尝试完，这部分信息不展示给用户
                        job.log(u'start job failed: %s (%d/%d)' % (e.message, index, len(accounts)), 'error')
                        continue
                    e.record_transaction(job.log, 'user')
                    job.log(u'start job failed: %s' % e.message, 'user')
                    job.update_status(StatusType.FAILED, CodeType.START_JOB_FAILED, e.message)
                    return False
                else:
                    # 更新步骤
                    job.update_job_step(StepType.EXECUTE_UNINSTALL_JOB)
                    task_inst_id = data.get('taskInstanceId')
                    break

        # 填充作业ID
        job.update_bk_job_id(task_inst_id)
        job.log(u'start job success，begin poll job status')

        # 更新步骤
        job.update_job_step(StepType.WAIT_AGENT)
        job.poll_agent_status(expected_status=0, need_remove=need_remove)

    except NginxSettingError as error:
        job.log(u'error: %s' % error.message, 'user')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)

    except NginxConnectionError as error:
        job.log(u'error: %s' % error.message, 'user')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)

    except Exception as err:
        job.log("{}: {}, please check Log in Developer Center.".format(CodeType.CELERY_TASK_EXCEPT, str(err)))
        job.log(u'System error: %s' % traceback.format_exc(), 'error')
        job.update_status(StatusType.FAILED, CodeType.CELERY_TASK_EXCEPT)
