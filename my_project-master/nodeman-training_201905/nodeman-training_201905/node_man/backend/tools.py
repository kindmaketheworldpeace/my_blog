# -*- coding: utf-8 -*-
"""
celery任务工具箱
"""

import os
import json
import base64
import urllib2
import requests

from common.log import logger
from node_man.component.esbclient import client
from node_man.component.exceptions import NginxConnectionError
from node_man.constants import (MAX_POLL_TIMES, JOB_SUCCESS,
                                CodeType, EXIT_CONDITIONS,
                                RECV_BUFLEN, StepType, AuthType,
                                DEFAULT_SCRIPT, OsType, SCRIPT_DICT, JobType, AIX_PKG_NAME)
from node_man.models import Job, KV, HostStatus, Cloud
from node_man.settings import REMOTE_PATH, SCRIPT_DIR, LOCAL_PATH, TMP
from node_man.utils.basic import safe_cast
from node_man.utils.simple_rsa import rsa_decrypt
from node_man.utils.ssh import inspector, ssh_login, SshMan


# from node_man.utils.wmiexec_helper import WmiExec


def get_script_content(os_type=OsType.LINUX, nginx_type='outer_url'):
    """
        获取远程安装脚本内容
        nginx_type:获取nginx配置的类型，默认是外网ip
    """

    SCRIPT = SCRIPT_DICT.get(os_type)
    NGINX_CFG = KV.get_nginx_config(nginx_type).split(',')[0]

    # 读取文件服务器中的安装脚本
    script_url = '{NGINX_CFG}/{SCRIPT}'.format(NGINX_CFG=NGINX_CFG, SCRIPT=SCRIPT)

    # raise exception to caller
    # script_content = requests.get(script_url).text
    try:
        script_content = urllib2.urlopen(script_url).read()
    except Exception as e:
        logger.error(u"download script file error %s" % e)
        raise NginxConnectionError("request url is %s" % script_url)
    return script_content


def create_pagent_install_script(job_id, script_name):
    """
    根据目标IP列表渲染得到install_pagent.sh
    """

    job = Job.objects.get(id=job_id)

    ip_list, key_list, host_content_list, key_content_list = [], [], [], []
    for host in job.get_job_hosts():
        password = rsa_decrypt(host.password) if host.password else ''
        key_content = host.key if host.auth_type == AuthType.KEY else ''
        identity = '/tmp/key_{}'.format(host.login_ip if host.login_ip else host.inner_ip) if host.auth_type == AuthType.KEY else password

        # 生成脚本模板参数
        host_content_list.append(
            '{LOGIN_IP} {CONN_IP} {DATA_IP} {PORT} {ACCOUNT} {IDENTITY} {OS_TYPE} {HAS_CYGWIN}'.format(
                LOGIN_IP=host.login_ip if host.login_ip else host.inner_ip,
                CONN_IP=host.inner_ip,
                DATA_IP=host.data_ip if host.data_ip else host.inner_ip,
                PORT=host.port,
                ACCOUNT=host.account,
                IDENTITY=identity,
                OS_TYPE=host.os_type.lower(),
                HAS_CYGWIN=host.has_cygwin)
        )

        # 拼接密钥
        if host.auth_type == AuthType.KEY:
            key_content_list.append(key_content)

    # raise exception to caller
    content = get_script_content(nginx_type='inner_url')

    # 替换主机列表信息及密钥信息
    content = content.replace('%%HOSTS_LIST%%', '\n'.join(host_content_list))
    content = content.replace('%%SECREY_STRING%%', '\n'.join(key_content_list).rstrip('\n'))
    content = content.encode('utf-8')

    # 生成脚本文件，内容base64编码
    with open(os.path.join(SCRIPT_DIR, script_name), 'w') as f:
        f.write(content)

    return content


def create_script_param(bk_cloud_id=-1, proxy_list=None, run_mode=None, mode=None, host=None, bk_supplier_id=0):
    """
    生成脚本参数，针对非直连模式
    :param proxy_list:proxy列表
    :param bk_cloud_id:平台id_开发商id
    :param run_mode: 0非直连，1直连
    :param mode:pa/agent
    """

    if run_mode == 1:
        # 直连agent 用nginx的内网配置
        NGINX_CFG = KV.get_nginx_config('inner_url')
        gse_cfg = KV.get_gse_config('inner_ip')
        param = '-m client -g {NGINX_CFG} -E {conn_ip} -D {data_ip} -I {bk_supplier_id}'.format(
            NGINX_CFG=NGINX_CFG,
            conn_ip=host.inner_ip,
            data_ip=host.data_ip if host.data_ip else host.inner_ip,
            bk_supplier_id=bk_supplier_id)
        if gse_cfg:
            param += " -A {gse_cfg}".format(gse_cfg=gse_cfg)
    else:
        # 非直连proxy/agent
        # 安装脚本用NGINX的内网IP，加速文件下载
        NGINX_CFG = KV.get_nginx_config('outer_url')
        gse_cfg = KV.get_gse_config('outer_ip')
        logger.warning(proxy_list)
        proxy_wanips = ','.join([proxy['outer_ip'] for proxy in proxy_list])
        proxy_lanips = ','.join([proxy['inner_ip'] for proxy in proxy_list])
        if mode == 'agent':
            # 非直连agent安装参数
            param = ' -m client -b -i {CLOUD_ID} ' \
                    '-w {PROXY_WANIP} -l {PROXY_LANIP} -g {NGINX_CFG} -I {bk_supplier_id}'.format(
                CLOUD_ID=bk_cloud_id,
                PROXY_WANIP=proxy_wanips,
                PROXY_LANIP=proxy_lanips,
                NGINX_CFG=NGINX_CFG,
                bk_supplier_id=bk_supplier_id
            )
        else:
            # 非直连proxy安装参数
            param = ' -m proxy -i {CLOUD_ID} -w {PROXY_WANIP} -E {conn_ip} -D {data_ip} -l {PROXY_LANIP}' \
                    ' -g {NGINX_CFG} -I {bk_supplier_id}'.format(
                CLOUD_ID=bk_cloud_id,
                PROXY_WANIP=proxy_wanips,
                PROXY_LANIP=proxy_lanips,
                NGINX_CFG=NGINX_CFG,
                conn_ip=host.inner_ip,
                data_ip=host.data_ip if host.data_ip else host.inner_ip,
                bk_supplier_id=bk_supplier_id
            )
            if gse_cfg:
                param += " -A {gse_cfg}".format(gse_cfg=gse_cfg)
    return param


#
# def make_install_cmd_list(job_task):
#     """
#     生成proxy安装命令及辅助命令序列
#     """
#
#     host = job_task.host
#     proxy_list = HostStatus.get_host_related_proxy_list(host)
#
#     # 直连proxy/agent
#     if Cloud.is_default_cloud(host.bk_cloud_id):
#         NGINX_CFG = KV.get_nginx_config('inner_ip').split(',')[0]
#         PARAM = create_script_param(host.bk_cloud_id, run_mode=1)
#     else:
#         # 非直连proxy
#         # 取NGINX外网IP作为文件服务器地址，仅用于下载脚本文件
#         NGINX_CFG = KV.get_nginx_config('outer_ip').split(',')[0]
#         PARAM = create_script_param(host.bk_cloud_id, proxy_list, run_mode=0, mode='proxy')
#
#     # 根据需要安装curl，风险 sudo apt-get install 需要认证
#     # install_curl = 'export LC_ALL=C; sudo apt-get update && sudo apt-get install -y curl || ' \
#     #               'apt-get update && apt-get install -y curl || ' \
#     #               'yum makecache && yum install -y curl || ' \
#     #               'pkg install -y curl'
#
#     install_curl = '''export LC_ALL=C;
#                     if which apt-get &>/dev/null; then
#                         sudo apt-get makecache
#                         sudo apt-get -y install wget
#                         sudo apt-get -y install curl
#                     elif which  yum &>/dev/null; then
#                         yum makecache
#                         yum install -y wget
#                         yum install -y curl
#                     elif which pkg &>/dev/null; then
#                         pkg install -y wget
#                         pkg install -y curl
#                     else
#                         false
#                     fi'''
#
#     curl_script = 'export LC_ALL=C; rm -f {SCRIPT}; curl -O http://{NGINX_CFG}/download/{SCRIPT}'.format(
#         NGINX_CFG=NGINX_CFG,
#         SCRIPT=DEFAULT_SCRIPT,
#         PARAM=PARAM)
#     chmod_cmd = 'chmod a+x ./{SCRIPT}'.format(SCRIPT=DEFAULT_SCRIPT)
#
#     # 务必指定绝对路径
#     install_cmd = 'export LC_ALL=C; {DST}/{SCRIPT} {PARAM}'.format(DST=REMOTE_PATH, PARAM=PARAM, SCRIPT=DEFAULT_SCRIPT)
#
#     # 批处理流程：创建目录->wget->install
#     cmds = [
#         '[ -d {DST} ] || mkdir -p {DST}'.format(DST=REMOTE_PATH),
#         'export LC_ALL=C; cd {DST} && pwd && ls -rtlh --color=never'.format(DST=REMOTE_PATH),
#         install_curl,
#         curl_script,
#         chmod_cmd,
#     ]
#
#     # 升级逻辑
#     if job_task.job.job_type in [
#         JobType.UPGRADE_PROXY,
#         JobType.UPGRADE_AGENT,
#         JobType.UPGRADE_PAGENT
#     ]:
#         install_cmd += ' -u'
#         cmds = []
#
#     # 脚本调用命令及调用前的辅助命令序列
#     return install_cmd, cmds


# def install_proxy_by_ssh(job_task):
#     """
#     SSH安装模式下的主任务流程控制
#     """
#     host = job_task.host
#     install_cmd, cmd_list = make_install_cmd_list(job_task)
#     job_task.log(u"create proxy install cmd list: %s" % '\n'.join(cmd_list), 'info')
#
#     # 更新步骤状态为SSH登录
#     job_task.update_step(StepType.SSH_LOGIN)
#     job_task.log(u"start ssh login.")
#     ssh, accessed, err_desc, err_code, = ssh_login(host)
#
#     # ssh登录失败
#     if accessed is False or ssh is None:
#         job_task.log(u"ssh login failed，error code【%s】：%s" % (err_code, err_desc))
#         return err_code, err_desc
#
#     job_task.log(u"ssh login success.")
#     chan = ssh.invoke_shell()
#     ssh_man = SshMan(chan, job_task.log)
#
#     # 一定要先设置一个干净的提示符号，否则会导致console_ready识别失效
#     ssh_man.set_prompt()
#     # 吃掉登录提示符
#     ssh_man.get_prompt()
#
#     # 执行辅助安装命令，更新步骤状态为下载安装包
#     job_task.update_step(StepType.INSTALL_DEP)
#     job_task.log(u"start run dependent cmd.")
#     for i, cmd in enumerate(cmd_list):
#         # job_task.log(u"run cmd【%s/%s】: %s" % (i + 1, len(cmd_list), json.dumps(cmd)))
#         is_cmd_started, output, err_code = ssh_man.send_cmd(cmd, host.account, host.password, True)
#
#         if is_cmd_started and err_code == CodeType.SUCCESS:
#             job_task.log(u'%s:execute success.' % (i + 1), 'info')
#         else:
#             job_task.log(u'%s:execute fail.' % (i + 1))
#             err_desc = u'install failed because failed cmd: %s' % cmd
#             job_task.log(u"is_cmd_started:%s, output:%s, code:%s" % (is_cmd_started, output, err_code))
#             break
#     else:
#         # 辅助命令执行完毕，更新当前状态为执行脚本
#         job_task.update_step(StepType.EXECUTE_SCRIPT)
#         job_task.log(u"prepare to call real install script【%s】" % json.dumps(install_cmd))
#
#         # 启动安装脚本 mark: account != username
#         is_cmd_started, output, err_code = ssh_man.send_cmd(
#             install_cmd,
#             host.account,
#             host.password,
#             False
#         )
#
#         # 等待脚本执行完毕
#         if is_cmd_started is True and err_code == CodeType.SUCCESS:
#             job_task.log(u"start install script success, ret code is【%s】" % err_code)
#             ssh_man.wait_for_output()
#
#             # 期望输出 install_success
#             while True:
#                 err_code, err_desc = inspector.fetch_code(output)
#
#                 # 安装成功
#                 if err_code == CodeType.SUCCESS:
#                     break
#
#                 # 出现一下任何一种情况，视为安装失败，结束ssh安装会话
#                 if err_code in EXIT_CONDITIONS:
#                     job_task.log(u"install failed error code is【%s】" % err_code)
#                     break
#
#                 # 减少打印量
#                 if err_code != CodeType.STILL_RUNNING:
#                     job_task.log(u"current task state is【%s -> %s】" % (err_code, err_desc))
#
#                 output = chan.recv(RECV_BUFLEN)
#                 job_task.log(output)
#         else:
#             err_desc = output
#
#     # 关闭chan/ssh
#     SshMan.safe_close(chan)
#     SshMan.safe_close(ssh)
#
#     return err_code, err_desc

#
# def install_proxy_by_wmiexec(job_task):
#     """
#     Wmiexec安装模式
#     """
#     wmi = WmiExec(job_task)
#     job_task.log(u"install proxy in wmiexec mode.")
#     return wmi.install_windows_agent()


# def install_aix_agent_by_ssh(job_task):
#     """
#     Aix下的agnet安装
#     """
#     aix_script_name = SCRIPT_DICT.get(OsType.AIX)
#     AIX_FILE_LIST = [AIX_PKG_NAME, aix_script_name]
#
#     host = job_task.host
#
#     def is_latest(file_path, md5_num):
#         pass
#
#     def prepare_aix_installer_files():
#         """从nginx下载aix安装包"""
#
#         NGINX_CFG = KV.get_nginx_config('inner_ip').split(',')[0]
#
#         for f in AIX_FILE_LIST:
#             # 本地只下载一次，校验MD5(TODO)
#             if os.path.exists(os.path.join(LOCAL_PATH, f)):
#                 job_task.log('find exist aix installer file: %s' % f)
#                 continue
#             job_task.log('get aix installer file: %s' % f)
#             # with requests.get('http://{}/download/{}'.format(NGINX_CFG, f), stream=True) as r:
#             r = urllib2.urlopen('http://{}/download/{}'.format(NGINX_CFG, f))
#             with open(os.path.join(LOCAL_PATH, f), 'wb') as f:
#                 f.write(r.read())
#
#     job_task.log(u"prepare aix installer files.")
#     prepare_aix_installer_files()
#
#     install_cmd = 'chmod +x {DST}/{SCRIPT} && {DST}/{SCRIPT} {PARAM}'.format(
#         DST='/tmp',
#         SCRIPT=aix_script_name,
#         PARAM=create_script_param(run_mode=1)
#     )
#
#     job_task.log(u'aix server locate in direct cloud area, install_cmd：%s' % install_cmd)
#
#     # 更新步骤状态为SSH登录
#     job_task.update_step(StepType.SSH_LOGIN)
#     job_task.log(u"start ssh login.")
#     ssh, accessed, err_desc, err_code, = ssh_login(host)
#
#     # ssh登录失败
#     if accessed is False or ssh is None:
#         job_task.log(u"ssh login failed，error code【%s】：%s" % (err_code, err_desc))
#         return err_code, err_desc
#
#     # 发送安装包和安装脚本
#     # scp = SCPClient(ssh.get_transport())
#     job_task.log(u"send files to aix server: %s." % host.inner_ip)
#     sftp = ssh.open_sftp()
#     for f in AIX_FILE_LIST:
#         # 发送压缩包
#         job_task.log(u"start send【%s】to【%s】." % (f, host.inner_ip))
#         sftp.put(os.path.join(LOCAL_PATH, f), os.path.join(TMP, f))
#         job_task.log(u"send【%s】to【%s】success." % (f, host.inner_ip))
#
#     # 执行安装脚本
#     job_task.log(u"ssh login success.")
#     chan = ssh.invoke_shell()
#     ssh_man = SshMan(chan, job_task.log)
#
#     # 一定要先设置一个干净的提示符号，否则会导致console_ready识别失效
#     ssh_man.set_prompt()
#     # 吃掉登录提示符
#     ssh_man.get_prompt()
#
#     # 执行辅助安装命令，更新步骤状态为下载安装包
#     job_task.update_step(StepType.INSTALL_DEP)
#     job_task.log(u"start run dependent cmd.")
#
#     # 辅助命令执行完毕，更新当前状态为执行脚本
#     job_task.update_step(StepType.EXECUTE_SCRIPT)
#     job_task.log(u"prepare to call real install script【%s】" % json.dumps(install_cmd))
#
#     # 启动安装脚本 mark: account != username
#     is_cmd_started, output, err_code = ssh_man.send_cmd(
#         install_cmd,
#         host.account,
#         host.password,
#         False
#     )
#
#     # 等待脚本执行完毕
#     if is_cmd_started is True and err_code == CodeType.SUCCESS:
#         job_task.log(u"start install script success, ret code is【%s】" % err_code)
#         ssh_man.wait_for_output()
#
#         # 期望输出 install_success
#         while True:
#             err_code, err_desc = inspector.fetch_code(output)
#
#             # 安装成功
#             if err_code == CodeType.SUCCESS:
#                 break
#
#             # 出现一下任何一种情况，视为安装失败，结束ssh安装会话
#             if err_code in EXIT_CONDITIONS:
#                 job_task.log(u"install failed error code is【%s】" % err_code)
#                 break
#
#             # 减少打印量
#             if err_code != CodeType.STILL_RUNNING:
#                 job_task.log(u"current task state is【%s -> %s】" % (err_code, err_desc))
#
#             output = chan.recv(RECV_BUFLEN)
#             job_task.log(output)
#     else:
#         # 脚本启动失败
#         err_desc = u"start install script failed: %s" % output
#         job_task.log(u"start install script failed【%s】，detail：%s" % (err_code, output))
#
#     # 关闭chan/ssh
#     SshMan.safe_close(chan)
#     SshMan.safe_close(ssh)
#
#     return err_code, err_desc


def get_ijob_result(task_instance_id, extra=None):
    """
    查询ijobs任务实例，获取ijobs任务的业务ID、步骤详情以及当前状态
    extra: 用于指定是否需要返回第一个block的第一个步骤的状态详情
    """

    # 查询作业
    res = client.job.get_task_result({'task_instance_id': task_instance_id})
    logger.info(u'get_ijob_result: task_instance_id=%s, res=%s' % (task_instance_id, res))

    # 查询作业步骤
    if res.get('result', False):
        task_info = res.get('data', {})
        task_instance = task_info.get('taskInstance', {})

        # 步骤详情查询参数blocks、任务结束标志、任务状态、ijobs业务id
        is_finished = task_info.get('isFinished')  # 任务是否结束
        status = task_instance.get('status', 0)  # 更新总任务状态
        if is_finished:
            is_ok = (status == JOB_SUCCESS)

            # 返回附加统计信息
            if extra:
                try:
                    blocks = task_info.get('blocks')
                    step_instance = blocks[0].get('stepInstances')[0]
                except Exception as e:
                    step_instance = {'text': e}
                    logger.error(u'get_ijob_result(Exception): %s' % e)
            else:
                step_instance = {}
        else:
            is_ok = False
            step_instance = {'text': u'ijob not finished.'}
    else:
        # 查询返回结果为False，这里认为任务未结束
        is_finished, is_ok = False, False
        logger.error(u'get_ijob_task_result(fail): task_instance_id=%s, msg=%s' % (
            task_instance_id, res.get('message')))
        step_instance = {'text': u'get_ijob_result failed: %s' % res.get('message')}

    return {
        'is_finished': is_finished,
        'is_ok': is_ok,
        'step_instance': step_instance,
    }


def get_agent_status(host, poll_status=None):
    """
    查询agent状态，返回1为连线ok
    """

    ip = host.get('inner_ip')
    bk_cloud_id = safe_cast(host.get('bk_cloud_id'), int)

    # 配置平台云区域ID=1 -->作业平台云区域ID=0
    bk_cloud_id = 0 if bk_cloud_id == 1 else bk_cloud_id
    kwargs = {
        'company_id': 0,  # 接口变更
        'app_id': host.get('biz_id'),
        "is_real_time": 1,
        "ip_infos": [
            {
                "ip": ip,
                "bk_cloud_id": bk_cloud_id
            }
        ]
    }

    # 支持状态轮训
    exist = 0
    retries = 0
    while retries < MAX_POLL_TIMES:
        retries += 1
        res = client.job.get_agent_status(kwargs)
        logger.info(u'获取下agent状态: kwargs=%s, res=%s' % (kwargs, res), 'info')
        if res.get('result', False):
            # 接口变更，返回数据携带bk_cloud_id
            result_dict = {item.get('ip'): item.get('status')
                           for item in res.get('data', [])}
            exist = result_dict.get(ip, 0)
        else:
            exist = 0
            logger.error(u'get_agent_status(fail)【kwargs=%s】: %s' %
                         (kwargs, res.get('message')))

        # 是否轮询
        if poll_status is None or exist == poll_status:
            break

    return exist
