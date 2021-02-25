# -*- coding: utf-8 -*-

import json

from node_man.backend.installers.installer import Installer

from node_man.constants import (CodeType, EXIT_CONDITIONS, RECV_BUFLEN, StepType)
from node_man.utils.ssh import inspector, ssh_login, SshMan

from node_man.constants import (DEFAULT_SCRIPT, JobType)
from node_man.models import KV, HostStatus, Cloud
from node_man.settings import REMOTE_PATH
from node_man.backend.tools import create_script_param


class LinuxInstaller(Installer):
    def __init__(self, job_task):
        self.job_task = job_task
        self.log = job_task.log
        super(LinuxInstaller, self).__init__()

    def make_install_cmd_list(self):
        """
        生成proxy安装命令及辅助命令序列
        """

        host = self.job_task.host
        bk_supplier_id = self.job_task.job.bk_supplier_id if self.job_task.job.bk_supplier_id else 0
        proxy_list = HostStatus.get_host_related_proxy_list(host)

        # 直连proxy/agent
        if Cloud.is_default_cloud(host.bk_cloud_id):
            NGINX_CFG = KV.get_nginx_config('inner_url').split(',')[0]
            PARAM = create_script_param(host.bk_cloud_id, run_mode=1, host=host,
                                        bk_supplier_id=bk_supplier_id)
        else:
            # 非直连proxy
            # 取NGINX外网IP作为文件服务器地址，仅用于下载脚本文件
            NGINX_CFG = KV.get_nginx_config('outer_url').split(',')[0]
            PARAM = create_script_param(host.bk_cloud_id, proxy_list, run_mode=0, mode='proxy', host=host,
                                        bk_supplier_id=bk_supplier_id)

        # 根据需要安装curl，风险 sudo apt-get install 需要认证
        # install_curl = 'export LC_ALL=C; sudo apt-get update && sudo apt-get install -y curl || ' \
        #               'apt-get update && apt-get install -y curl || ' \
        #               'yum makecache && yum install -y curl || ' \
        #               'pkg install -y curl'

        # install_curl = '''LC_ALL=C
        #                 if which apt-get &>/dev/null; then
        #                     sudo apt-get makecache
        #                     sudo apt-get -y install wget
        #                     sudo apt-get -y install curl
        #                 elif which  yum &>/dev/null; then
        #                     yum makecache
        #                     yum install -y wget
        #                     yum install -y curl
        #                 elif which pkg &>/dev/null; then
        #                     pkg install -y wget
        #                     pkg install -y curl
        #                 else
        #                     false
        #                 fi'''

        install_wget_debian = '''which apt-get &>/dev/null || { sudo LC_ALL=C apt-get makecache && sudo LC_ALL=C apt-get -y install wget curl; }'''
        install_wget_centos = '''which yum &>/dev/null || { sudo LC_ALL=C yum makecache && sudo LC_ALL=C yum -y install wget curl; }'''
        install_wget_bsd = '''which pkg &>/dev/null || sudo LC_ALL=C pkg install -y wget'''

        clear_old_file = 'rm -f {DST}/{SCRIPT}'.format(DST=REMOTE_PATH, SCRIPT=DEFAULT_SCRIPT)

        curl_script = 'LC_ALL=C wget -O  {DST}/{SCRIPT} {NGINX_CFG}/{SCRIPT}'.format(
            NGINX_CFG=NGINX_CFG,
            DST=REMOTE_PATH,
            SCRIPT=DEFAULT_SCRIPT)

        chmod_cmd = 'chmod a+x {DST}/{SCRIPT}'.format(DST=REMOTE_PATH, SCRIPT=DEFAULT_SCRIPT)

        # 务必指定绝对路径
        install_cmd = 'LC_ALL=C {DST}/{SCRIPT} {PARAM}'.format(DST=REMOTE_PATH, PARAM=PARAM,
                                                               SCRIPT=DEFAULT_SCRIPT)

        # 批处理流程：创建目录->wget->install
        cmds = [
            '[ -d {DST} ] || mkdir -p {DST}'.format(DST=REMOTE_PATH),
            'LC_ALL=C ls -rtlh --color=never'.format(DST=REMOTE_PATH),
            # install_curl,
            install_wget_centos,
            install_wget_debian,
            install_wget_bsd,
            clear_old_file,
            curl_script,
            chmod_cmd,
        ]

        # 升级逻辑
        if self.job_task.job.job_type in [
            JobType.UPGRADE_PROXY,
            JobType.UPGRADE_AGENT,
            JobType.UPGRADE_PAGENT
        ]:
            install_cmd += ' -u'
            cmds = [
                clear_old_file,
                curl_script,
                chmod_cmd,
            ]

        # 脚本调用命令及调用前的辅助命令序列
        return install_cmd, cmds

    def execute(self):
        """
        SSH安装模式下的主任务流程控制
        """
        host = self.job_task.host
        install_cmd, cmd_list = self.make_install_cmd_list()
        self.job_task.log(u"create proxy install cmd list: %s" % '\n'.join(cmd_list), 'info')

        # 更新步骤状态为SSH登录
        self.job_task.update_step(StepType.SSH_LOGIN)
        self.job_task.log(u"start ssh login.")
        ssh, accessed, err_desc, err_code, = ssh_login(host)

        # ssh登录失败
        if accessed is False or ssh is None:
            self.job_task.log(u"ssh login failed，error code【%s】：%s" % (err_code, err_desc))
            return err_code, err_desc

        self.job_task.log(u"ssh login success.")
        chan = ssh.invoke_shell()
        ssh_man = SshMan(chan, self.job_task.log)

        # 一定要先设置一个干净的提示符号，否则会导致console_ready识别失效
        ssh_man.set_prompt()
        # 吃掉登录提示符
        ssh_man.get_prompt()

        # 执行辅助安装命令，更新步骤状态为下载安装包
        self.job_task.update_step(StepType.INSTALL_DEP)
        self.job_task.log(u"start run dependent cmd.")
        for i, cmd in enumerate(cmd_list):
            # self.job_task.log(u"run cmd【%s/%s】: %s" % (i + 1, len(cmd_list), json.dumps(cmd)))
            is_cmd_started, output, err_code = ssh_man.send_cmd(cmd, host.account, host.password, True)

            if is_cmd_started and err_code == CodeType.SUCCESS:
                self.job_task.log(u'%s:execute success.' % (i + 1), 'info')
            else:
                self.job_task.log(u'%s:execute fail.' % (i + 1))
                err_desc = u'install failed because failed cmd: %s' % cmd
                self.job_task.log(u"is_cmd_started:%s, output:%s, code:%s" % (is_cmd_started, output, err_code))
                break
        else:
            # 辅助命令执行完毕，更新当前状态为执行脚本
            self.job_task.update_step(StepType.EXECUTE_SCRIPT)
            self.job_task.log(u"prepare to call real install script【%s】" % json.dumps(install_cmd))

            # 启动安装脚本 mark: account != username
            is_cmd_started, output, err_code = ssh_man.send_cmd(
                install_cmd,
                host.account,
                host.password,
                False
            )

            # 等待脚本执行完毕
            if is_cmd_started is True and err_code == CodeType.SUCCESS:
                self.job_task.log(u"start install script success, ret code is【%s】" % err_code)
                ssh_man.wait_for_output()

                # 期望输出 install_success
                while True:
                    err_code, err_desc = inspector.fetch_code(output)

                    # 安装成功
                    if err_code == CodeType.SUCCESS:
                        break

                    # 出现一下任何一种情况，视为安装失败，结束ssh安装会话
                    if err_code in EXIT_CONDITIONS:
                        self.job_task.log(u"install failed error code is【%s】" % err_code)
                        break

                    # 减少打印量
                    if err_code != CodeType.STILL_RUNNING:
                        self.job_task.log(u"current task state is【%s -> %s】" % (err_code, err_desc))

                    output = chan.recv(RECV_BUFLEN)
                    self.job_task.log(output)
            else:
                err_desc = output

        # 关闭chan/ssh
        SshMan.safe_close(chan)
        SshMan.safe_close(ssh)

        return err_code, err_desc
