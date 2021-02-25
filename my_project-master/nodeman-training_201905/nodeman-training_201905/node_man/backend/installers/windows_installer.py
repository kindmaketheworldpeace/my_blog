# -*- coding: utf-8 -*-
import os
import sys

from node_man.backend.installers.installer import Installer
from node_man.constants import StepType, CodeType
from node_man.models import KV
from node_man.settings import ZIP_PATH
from node_man.utils.basic import extract_tarfile
from node_man.utils.wmiexec import execute_cmd, put_file

reload(sys)
sys.setdefaultencoding('utf8')

# 目标安装目录
DEST_DIR = "c:\\"
INSTALL_CMD = "%s\\gseagentw\\gse_win_daemon.exe -install" % DEST_DIR

# 参考命令，暂不使用
MKDIR_CMD = "mkdir {dst_dir} > nul".format(dst_dir=DEST_DIR)
CLEAN_CMD = "del /Q %s\\gseagentw*.* >nul" % DEST_DIR
SERVICE_GET_CMD = "wmic service get Name /value|findstr gse 2>nul"
REMOVE_CMD = "c:\\gseagentw\\gse_win_daemon.exe -remove"
FIND_DIR_CMD = "dir C: /AD /B |findstr gse 2>nul"
RD_CMD = "rd /s /q c:\\ 2>nul"

# 检测系统总线64/32
ARC_DETECT_CMD = "echo %PROCESSOR_ARCHITECTURE%"
ARC_TO_PKG = {
    "32": "gse_client-windows-x86.tgz",
    "64": "gse_client-windows-x86_64.tgz",
}

from node_man.utils.simple_rsa import rsa_decrypt


class WindowsInstaller(Installer):
    def __init__(self, job_task, domain=""):
        self.job_task = job_task
        self.log = job_task.log
        self.host = self.job_task.host
        self.username = self.host.account
        self.password = rsa_decrypt(self.host.password)
        self.inner_ip = self.host.inner_ip
        self.login_ip = self.host.login_ip
        self.data_ip = self.host.data_ip
        self.bk_cloud_id = self.host.bk_cloud_id
        self.bk_biz_id = self.host.bk_biz_id
        self.domain = domain
        self.local_tmp_path = ZIP_PATH
        self.nginx_cfg = KV.get_nginx_config('inner_url').split(',')[0]

    def uninstall_windows_agent(self):
        """卸载agent"""

        # find gse service and remove it
        res = execute_cmd(SERVICE_GET_CMD, self.login_ip or self.inner_ip, self.username, self.password, self.domain)
        if res["result"] and res["data"]:
            remove_res = execute_cmd(REMOVE_CMD, self.login_ip or self.inner_ip, self.username, self.password,
                                     self.domain)
            if remove_res["result"] and not remove_res["data"]:
                self.log("agent remove success")
            else:
                return {"result": False, "message": "agent remove failed"}
        elif not res["result"]:
            return {"result": False, "message": "server connect failed"}

        # find directory in c pan and find gse dir to delete
        find_res = execute_cmd(FIND_DIR_CMD, self.login_ip or self.inner_ip, self.username, self.password, self.domain)
        if find_res["result"] and find_res["data"]:
            rd_res = execute_cmd(RD_CMD, self.login_ip or self.inner_ip, self.username, self.password, self.domain)
            if rd_res["result"] and not rd_res["data"]:
                self.log("agent file folder delete success")
            else:
                return {"result": False, "message": "agent file folder delete failed"}
        elif not find_res["result"]:
            return {"result": False, "message": "server connect failed"}

        return {"result": True, "message": "agent clean success"}

    def prepare_agent_file(self):
        """下载安装文件包到本地"""

        file_list = ['direct_non_cygwin.tgz'] + ARC_TO_PKG.values()

        self.prepare_installer_files(file_list)

        # 解压工具包 TODO 选择性解压
        extract_tarfile((os.path.join(self.local_tmp_path, 'direct_non_cygwin.tgz')))

    def transfer_agent_file(self, arc):
        """上传agent安装包并解压"""

        upload_file_list = [
            '7z.exe',
            '7z.dll',
            'normaliz.dll',
            'winagent_install.zip',
            ARC_TO_PKG.get(arc)
        ]

        UNZIP_CMD = "{}7z.exe -y x winagent_install.zip -oC:\\".format(DEST_DIR)

        try:
            # 准备本地文件
            self.log('prepare local file')
            self.prepare_agent_file()
            self.log('local file ready, begin to upload')

            # 文件上传
            for f in upload_file_list:
                res = put_file(os.path.join(ZIP_PATH, f), DEST_DIR,
                               self.login_ip or self.inner_ip,
                               self.username,
                               self.password,
                               self.domain)
                if res["result"]:
                    self.log("put file %s success, detail: \n%s" % (f, res.get('data')))
                else:
                    return {"result": False, "message": "put file %s failed" % f}

            # 解压安装包
            self.log('unzip: %s' % UNZIP_CMD)
            res = execute_cmd(UNZIP_CMD, self.login_ip or self.inner_ip, self.username, self.password, self.domain)

            if res["result"]:
                self.log("unzip package success")
                return {"result": True, "message": "file upload success"}

            # 解压失败
            return {"result": False, "message": "unzip package failed"}

        except Exception as e:
            self.log("file upload failed: %s" % e, 'error')
            return {"result": False, "message": "file upload exception: %s" % e}

    def detect_windows_arc(self):
        # 32/64位判定
        res = execute_cmd(ARC_DETECT_CMD, self.login_ip or self.inner_ip, self.username, self.password, self.domain)
        self.log('%s(%s:%s): %s' % (ARC_DETECT_CMD, self.login_ip or self.inner_ip, self.username, res))
        if res["result"]:
            arc = res["data"]
            self.log('get system arc success')
            # 区分32/64位安装包
            if "32" in arc:
                arc = "32"
                self.log("windows system arc is: %s" % arc)
            elif "64" in arc:
                arc = "64"
                self.log("windows system arc is: %s" % arc)
            else:
                self.log("windows system arc not detected: %s" % arc)
                return {"result": False, "message": "windows system arc not detected"}
        else:
            self.log("get windows system arc failed: %s" % res)
            return {"result": False, "message": "get windows system arc failed"}

        return {"result": True, "data": arc}

    def execute(self):
        """执行agent安装命令
            32/64位判定 => 创建目录c:\gse => 上传文件 => 启动安装命令 => 清理安装包
            32/64位判定 => 创建目录c:\gse => 下载文件 => 上传文件 => 启动安装命令 => 清理安装包

            1. 下载并解压 direct_non_cygwin.tgz
            2. 下载gse_client-windows*.tgz
            3. 分发 gse_client-windows*.tgz, 7z.exe *.dll winagent_install.zip 到目标 windows 机器
            4. 在目标 windows 机器上远程执行(解压): 7z.exe -y x windows_install.zip -oC:\\
            5. 远程执行:
            winagent_install\gse_install.bat $TAG_REMOVE $IP $CLOUD_ID
        """
        try:
            self.job_task.update_step(StepType.DETECT_WIN_ARC)
            res = self.detect_windows_arc()
            if res['result'] is False:
                return CodeType.DETECT_ARC_FAILED, res.get('message')

            # 上传文件并解压
            arc = res.get('data')
            self.log("windows system arc: %s" % arc)

            self.job_task.update_step(StepType.UPLOAD_FILE)
            res = self.transfer_agent_file(arc)
            if res["result"] is False:
                self.log("upload file failed: %s" % res.get('message'))
                return CodeType.UPLOAD_FAILED, res.get('message')
            self.log("upload file success: %s" % res)

            # 启动安装脚本
            install_cmd = "{}winagent_install\\gse_install.bat -o {} -i {} -w {} -l {} -I {} -D {} -E {}".format(DEST_DIR,
                                                                                self.inner_ip,
                                                                                self.bk_cloud_id,
                                                                                "proxy_wanip_placeholder",
                                                                                "proxy_lanip_placeholder",
                                                                                self.bk_biz_id,
                                                                                self.data_ip,
                                                                                self.inner_ip)
            self.log(install_cmd)

            self.job_task.update_step(StepType.EXECUTE_SCRIPT)
            res = execute_cmd(install_cmd, self.login_ip or self.inner_ip, self.username, self.password, self.domain)

            # 安装成功
            self.job_task.update_step(StepType.SCRIPT_DONE)
            if res["result"] and res["data"].find("setup done") != -1:
                self.log("agent install success: %s" % res)
                return CodeType.SUCCESS, "agent installed success"

            return CodeType.INSTALL_FAILED, "agent install failed: %s" % res

        except Exception as e:
            self.log("agent install failed: %s" % e, 'error')
            return CodeType.CELERY_TASK_EXCEPT, "agent install exception: %s" % e
