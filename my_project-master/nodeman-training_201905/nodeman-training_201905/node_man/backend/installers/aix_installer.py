# -*- coding: utf-8 -*-
import os
import urllib2
import json

from node_man.backend.installers.installer import Installer

from node_man.utils.ssh import inspector, ssh_login, SshMan
from node_man.backend.tools import create_script_param

from node_man.constants import (CodeType, EXIT_CONDITIONS, RECV_BUFLEN, StepType, OsType, SCRIPT_DICT, AIX_PKG_NAME)
from node_man.models import KV
from node_man.settings import LOCAL_PATH, TMP


class AixInstaller(Installer):
    def __init__(self, job_task):
        self.job_task = job_task
        self.log = job_task.log
        self.aix_script_name = SCRIPT_DICT.get(OsType.AIX)
        self.AIX_FILE_LIST = [AIX_PKG_NAME, self.aix_script_name]
        self.local_tmp_path = LOCAL_PATH
        self.nginx_cfg = KV.get_nginx_config('inner_url').split(',')[0]
        super(AixInstaller, self).__init__()

    def execute(self):
        """
        Aix下的agnet安装
        """
        host = self.job_task.host

        self.job_task.log(u"prepare aix installer files.")
        # self.prepare_aix_installer_files()
        self.prepare_installer_files(self.AIX_FILE_LIST)
        self.job_task.log(u"aix installer files prepared.")

        install_cmd = 'chmod +x {DST}/{SCRIPT} && {DST}/{SCRIPT} {PARAM}'.format(
            DST='/tmp',
            SCRIPT=self.aix_script_name,
            PARAM=create_script_param(run_mode=1, host=host)
        )

        self.job_task.log(u'aix server locate in direct cloud area, install_cmd：%s' % install_cmd)

        # 更新步骤状态为SSH登录
        self.job_task.update_step(StepType.SSH_LOGIN)
        self.job_task.log(u"start ssh login.")
        ssh, accessed, err_desc, err_code, = ssh_login(host)

        # ssh登录失败
        if accessed is False or ssh is None:
            self.job_task.log(u"ssh login failed，error code【%s】：%s" % (err_code, err_desc))
            return err_code, err_desc

        # 发送安装包和安装脚本
        # scp = SCPClient(ssh.get_transport())
        self.job_task.log(u"send files to aix server: %s." % host.inner_ip)
        sftp = ssh.open_sftp()
        for f in self.AIX_FILE_LIST:
            # 发送压缩包
            self.job_task.log(u"start send【%s】to【%s】." % (f, host.inner_ip))
            sftp.put(os.path.join(LOCAL_PATH, f), os.path.join(TMP, f))
            self.job_task.log(u"send【%s】to【%s】success." % (f, host.inner_ip))

        # 执行安装脚本
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
            # ssh_man.wait_for_output()

            # 期望输出 install_success
            while True:
                self.job_task.log(u"poll for err code, output is: %s" % output)
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
            # 脚本启动失败
            err_desc = u"start install script failed: %s" % output
            self.job_task.log(u"start install script failed【%s】，detail：%s" % (err_code, output))

        # 关闭chan/ssh
        SshMan.safe_close(chan)
        SshMan.safe_close(ssh)

        return err_code, err_desc
