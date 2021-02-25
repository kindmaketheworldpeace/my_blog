# -*- coding: utf-8 -*-

"""
ssh登录与命令交互功能单元
"""

import re
import socket
import time
import traceback
from StringIO import StringIO

import paramiko

from common.log import logger
from node_man.constants import (SLEEP_INTERVAL, RECV_BUFLEN, MAX_WAIT_OUTPUT,
                                RECV_TIMEOUT, SSH_CON_TIMEOUT, CodeType, AuthType)
from node_man.utils.basic import safe_cast
from node_man.utils.simple_rsa import rsa_encrypt, rsa_decrypt

paramiko.util.log_to_file('paramiko_log.txt')

# public symbols
__all__ = ["ssh_login", "SshMan"]

# 去掉回车、空格、颜色码
CLEAR_CONSOLE_RE = re.compile(r'\\u001b\[\D{1}|\[\d{1,2}\D?|\\u001b\[\d{1,2}\D?~?|\r|\n|\s{1,}', re.I | re.U)
# 去掉其他杂项
CLEAR_MISC_RE = re.compile(r'\$.{0,1}\[\D{1}', re.I | re.U)
# 换行转换
LINE_BREAK_RE = re.compile(r'\r\n|\r|\n', re.I | re.U)


def ssh_login(host, timeout=SSH_CON_TIMEOUT):
    """
    ssh登录认证
    host: {
        'inner_ip': '',
        'outer_ip': '',
        'account': '',
        'port': '',
        'auth_type': 'PASSWORD',
        'password': '',
        'key': ''
    }
    """

    ssh = None
    port, account, password, auth_type = (
        safe_cast(host.port, int),
        host.account, host.password, host.auth_type
    )
    ip = host.outer_ip or host.login_ip or host.inner_ip

    try:
        logger.info(u'【%s】create ssh client' % ip)
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 密钥认证
        if auth_type == AuthType.KEY:

            key_file = StringIO(host.key)

            # 尝试rsa登录
            key_type = 'r'
            try:
                pkey = paramiko.RSAKey.from_private_key(key_file)
            except paramiko.PasswordRequiredException:
                logger.error(u'【%s】RSAKey need password!' % ip)
                pkey = paramiko.RSAKey.from_private_key(key_file, password)

            # 尝试dsa登录
            except paramiko.SSHException:
                key_type = 'd'
                try:
                    pkey = paramiko.DSSKey.from_private_key(key_file)
                except paramiko.PasswordRequiredException:
                    logger.info(u'【%s】DSAKey need password!' % ip)
                    pkey = paramiko.DSSKey.from_private_key(key_file, password)

            logger.info(u'【%s】: login by %ssa key, hostname=%s, username=%s, port=%s' %
                        (ip, key_type, ip, account, port))
            ssh.connect(hostname=ip, username=account, port=port, pkey=pkey, timeout=timeout)

        # 密码认证
        elif auth_type == AuthType.PASSWORD:
            password = rsa_decrypt(password)
            ssh.connect(ip, port, account, password, timeout=timeout)
        else:
            msg = u'SSH authentication method not supported. %s:(%s)' % (ip, auth_type)
            logger.warning(msg)
            return ssh, False, msg, CodeType.SSH_LOGIN_TIMEOUT  # 不支持的认证方式

    except paramiko.BadAuthenticationType as e:
        try:
            #  SSH AUTH WITH PAM
            def handler(title, instructions, fields):
                resp = []

                if len(fields) > 1:
                    raise paramiko.SSHException('Fallback authentication failed.')

                if len(fields) == 0:
                    # for some reason, at least on os x, a 2nd request will
                    # be made with zero fields requested.  maybe it's just
                    # to try to fake out automated scripting of the exact
                    # type we're doing here.  *shrug* :)
                    return resp

                for pr in fields:
                    if pr[0].strip() == "Username:":
                        resp.append(account)
                    elif pr[0].strip() == "Password:":
                        resp.append(password)

                logger.warning('SSH auth with interactive: %s' % resp)

                return resp

            ssh_transport = ssh.get_transport()
            if ssh_transport is None:
                logger.error('get_transport is None')
                ssh_transport = paramiko.Transport((ip, port))

            try:
                ssh_transport = paramiko.Transport((ip, port))
                ssh._transport = ssh_transport
                ssh_transport.start_client()
            except Exception as e:
                logger.error(e)

            ssh_transport.auth_interactive(account, handler)

            return ssh, True, 'ssh interactive success', CodeType.SUCCESS

        except paramiko.SSHException:
            logger.error('attempt failed; just raise the original exception')
            raise e

    except paramiko.BadHostKeyException, e:
        SshMan.safe_close(ssh)
        msg = u'SSH authentication key could not be verified.- %s@%s:%s - exception: %s' % \
              (account, ip, port, e)
        logger.warning(msg)
        return ssh, False, msg, CodeType.SSH_LOGIN_KEY_ERR  # 密码错或者用户错
    except paramiko.AuthenticationException, e:
        SshMan.safe_close(ssh)
        msg = u'SSH authentication failed.- %s@%s:%s - exception: %s' % (account, ip, port, e)
        logger.warning(msg)
        return ssh, False, msg, CodeType.SSH_WRONG_PASSWORD  # 密码错或者用户错(Authentication failed)
    except paramiko.SSHException, e:
        SshMan.safe_close(ssh)
        msg = u'SSH connect failed.- %s@%s:%s - exception: %s' % (account, ip, port, e)
        logger.warning(msg)
        return ssh, False, msg, CodeType.SSH_LOGIN_EXCEPT  # 登录失败，原因可能有not a valid RSA private key file
    except socket.error, msg:
        SshMan.safe_close(ssh)
        msg = u'TCP connect failed, timeout(%s) - %s@%s:%s' % (msg, account, ip, port)
        logger.warning(msg)
        return ssh, False, msg, CodeType.SOCKET_TIMEOUT  # 超时
    # except Exception, e:
    #     SshMan.safe_close(ssh)
    #     msg = u'ssh_login exception:(%s:%s): %s' % (ip, port, e)
    #     logger.error(u'ssh_login exception：%s' % traceback.format_exc())
    #     return ssh, False, msg, CodeType.CELERY_TASK_EXCEPT  # 程序异常
    else:
        msg = u'%s@%s:%s - auth success.' % (account, ip, port)
        return ssh, True, msg, CodeType.SUCCESS


class Inspector(object):
    """
    关键字处理，捕捉ssh及脚本相关输出并判定
    """

    @staticmethod
    def clear(s):
        """
        过滤console输出，回车、空格、颜色码等
        """

        try:
            # 尝试clear，出现异常（编码错误）则返回原始字符串
            _s = CLEAR_CONSOLE_RE.sub('', s)
            _s = CLEAR_MISC_RE.sub('$', _s)
        except Exception as e:
            _s = s
            logger.error(u'clear(Exception):%s' % e)
        return _s

    @staticmethod
    def clear_yes_or_no(s):
        return s.replace('yes/no', '').replace("'yes'or'no':", '')

    def is_wait_password_input(self, buff):
        buff = self.clear(buff)
        return buff.endswith("assword:") or buff.endswith("Password:")

    def is_too_open(self, buff):
        buff = self.clear(buff)
        return buff.find('tooopen') != -1 or buff.find('ignorekey') != -1

    def is_permission_denied(self, buff):
        buff = self.clear(buff)
        return buff.find('Permissiondenied') != -1

    def is_public_key_denied(self, buff):
        buff = self.clear(buff)
        return buff.find('Permissiondenied(publickey') != -1

    def is_invalid_key(self, buff):
        buff = self.clear(buff)
        return buff.find('passphraseforkey') != -1

    def is_timeout(self, buff):
        buff = self.clear(buff)
        return buff.find('lostconnectinfo') != -1 or \
               buff.find('Noroutetohost') != -1 or \
               buff.find('Connectiontimedout') != -1 or \
               buff.find('Connectiontimeout') != -1

    def is_key_login_required(self, buff):
        buff = self.clear(buff)
        return not buff.find('publickey,gssapi-keyex,gssapi-with-mic') == -1

    def is_refused(self, buff):
        buff = self.clear(buff)
        return not buff.find('Connectionrefused') == -1

    def is_fingerprint(self, buff):
        buff = self.clear(buff)
        return not buff.find('fingerprint:') == -1

    def is_wait_known_hosts_add(self, buff):
        buff = self.clear(buff)
        return not buff.find('tothelistofknownhosts') == -1

    def is_yes_input(self, buff):
        buff = self.clear(buff)
        return not buff.find('yes/no') == -1 or not buff.find("'yes'or'no':") == -1

    def is_console_ready(self, buff):
        buff = self.clear(buff)
        return buff.endswith('#') or buff.endswith('$') or buff.endswith('>')

    def has_lastlogin(self, buff):
        buff = self.clear(buff)
        return buff.find('Lastlogin') != -1

    def is_no_such_file(self, buff):
        buff = self.clear(buff)
        return not buff.find('Nosuchfileordirectory') == -1

    def is_cmd_not_found(self, buff):
        buff = self.clear(buff)
        return not buff.find('Commandnotfound') == -1

    def is_transported_ok(self, buff):
        buff = self.clear(buff)
        return buff.find('100%') != -1

    def is_curl_failed(self, buff):
        return buff.find('failedconnectto') != -1 or buff.find('connectiontimedout') != -1 or buff.find(
            'couldnotreso') != -1 or buff.find('connectionrefused') != -1 or buff.find("couldn'tconnect") != -1

    # 脚本输出解析方式
    def is_setup_done(self, buff):
        return buff.find("setup done") != -1 and buff.find("install_success") != -1

    def is_setup_failed(self, buff):
        return buff.find("setup failed") != -1

    def parse_err_msg(self, buff):
        return buff.split('--')[1]

    @staticmethod
    def fetch_code(res):
        """
        关键字捕捉判定（仅适用于安装proxy和直连agent）
        """
        if inspector.is_cmd_not_found(res):
            return CodeType.COMMAND_NOT_FOUND, CodeType.COMMAND_NOT_FOUND
        elif inspector.is_setup_done(res):
            return CodeType.SUCCESS, inspector.parse_err_msg(res)
        elif inspector.is_setup_failed(res):
            return CodeType.INSTALL_FAILED, inspector.parse_err_msg(res)
        else:
            return CodeType.STILL_RUNNING, ''

    def is_cmd_started_on_aix(self, cmd, output):
        """
        在aix机器上，输出命令的显示返回的下划线会包含特殊字符在下划线前。此方法用字母类子串来判断。
        :param cmd:
        :param output:
        :return:
        """
        cmd_chars = ''.join(c for c in cmd if c.isalpha())
        output_chars = ''.join(c for c in output if c.isalpha())
        is_common_substring = re.search('\w*'.join(list(cmd_chars)), output_chars)
        return is_common_substring or (cmd_chars in output_chars) or (cmd_chars.startswith(output_chars))

# 状态检测
inspector = Inspector()


class SshMan(object):
    """
    SshMan，负责SSH终端命令交互
    """

    def __init__(self, chan, log):
        self.set_proxy_prompt = 'export PS1="[\u@\h_BKproxy \W]\$"'

        # 初始化ssh会话
        self.chan = chan
        self.log = log
        self.setup_channel()

    def setup_channel(self, blocking=0, timeout=-1):
        """
            # settimeout(0) -> setblocking(0)
            # settimeout(None) -> setblocking(1)
        """
        # set socket read time out
        self.chan.setblocking(blocking=blocking)
        timeout = RECV_TIMEOUT if timeout < 0 else timeout
        self.chan.settimeout(timeout=timeout)

    def get_sys_type(self):
        """
        获取系统类型：ubuntu/otherlinux/windows
        """

        self.chan.sendall('cat /proc/version')
        self.wait_for_output()
        buff = self.wait_for_cmd()
        buff = buff.lower()
        if buff.find('ubuntu'):
            sys_type = 'ubuntu'
        elif buff.find('linux'):
            sys_type = 'other'
        else:
            sys_type = 'windows'
        return sys_type

    def send_cmd(self, cmd, account, password, wait_console_ready=True):
        """
        用指定账户user发送命令cmd
        """

        password_for = ('passwordfor%s:' % account).encode()

        # 根据用户名判断是否采用sudo
        if account not in ['root', 'Administrator']:
            try:
                if password and password.strip() != '':
                    password = rsa_decrypt(password)
            except:
                self.log(u'decrypt password error: %s' % password, 'warning')

            cmd = 'sudo %s' % cmd
            self.log(u'sudo(%s): %s' % (account, cmd))

        # 增加回车符
        cmd = cmd if cmd.endswith('\n') else '%s\n' % cmd

        # 发送命令并等待结束
        cmd_cleared = inspector.clear(cmd)
        self.chan.sendall(cmd)
        self.wait_for_output()
        self.log(u'start cmd：【%s】and wait for cmd finished.' % cmd, 'info')

        cmd_sent, cmd_received = False, False
        output, buff = '', ''
        while True:
            time.sleep(SLEEP_INTERVAL)
            try:
                output = self.chan.recv(RECV_BUFLEN)
                # 剔除空格、回车和换行
                _output = inspector.clear(output)
                self.log(output)

            except socket.timeout:
                self.log(u'recv socket timeout after %s seconds' % RECV_TIMEOUT, 'error')
                return False, output, CodeType.UNEXPECTED_RETURN
            except Exception, e:
                self.log(u'recv exception: %s' % e, 'error')
                return False, output, CodeType.CELERY_TASK_EXCEPT

            # [sudo] password for vagrant:
            if _output.endswith(password_for):
                if not cmd_sent:
                    cmd_sent = True
                    self.chan.sendall(password + '\n')
                    time.sleep(SLEEP_INTERVAL)
                else:
                    self.log(u'password error，sudo failed')
                    return False, output, CodeType.SSH_WRONG_PASSWORD
            elif _output.find('tryagain') != -1 or _output.find('incorrectpassword') != -1:
                if cmd_sent:
                    self.log(u'password error，sudo failed')
                    return False, output, CodeType.SSH_WRONG_PASSWORD
            elif inspector.is_curl_failed(_output):
                return False, output, CodeType.CURL_FILE_FAILED
            elif inspector.is_no_such_file(_output):
                return False, output, CodeType.FILE_DOES_NOT_EXIST
            elif inspector.is_console_ready(_output):
                return True, output, CodeType.SUCCESS
            elif _output.find(cmd_cleared) != -1 or cmd_cleared.startswith(_output):
                cmd_received = True
                self.log(u'cmd started.', 'info')
                continue
            elif inspector.is_cmd_started_on_aix(cmd_cleared, _output):
                cmd_received = True
                self.log(u'cmd started.', 'info')
                continue
            elif _output and cmd_received:
                if not wait_console_ready:
                    self.log(u'no need to wait cmd run over.')
                    return True, output, CodeType.SUCCESS


    def get_and_set_prompt(self):
        """
        尝试设置并获取终端提示符
        """

        old_prompt, prompt = '', ''
        try:
            old_prompt = self.get_prompt()
            self.set_prompt(self.set_proxy_prompt)

            prompt = self.get_prompt()
            is_prompt_set = (old_prompt != prompt)
        except Exception as e:
            stack_info = ''.join(traceback.format_stack())
            self.log(u"get_and_set_prompt: error=%s, stack=%s" % (e, stack_info), 'error')
            prompt = old_prompt
            is_prompt_set = False

        return is_prompt_set, prompt

    def wait_for_cmd(self):
        """
        等待命令执行结束，标志为 # 或 $ 或 >
        """

        # 等待命令执行完毕，返回命令提示符信息
        buff, res = '', ''
        while not inspector.is_console_ready(res):
            time.sleep(SLEEP_INTERVAL)
            res = self.chan.recv(RECV_BUFLEN)
            buff += res
        return buff

    def wait_for_output(self):
        """
        等待通道标准输出可读，重试32次
        """

        cnt = 0
        while not self.chan.recv_ready():
            time.sleep(SLEEP_INTERVAL)
            cnt += 1
            if cnt > MAX_WAIT_OUTPUT:  # 32
                break

    def get_prompt(self):
        """
        尝试获取终端提示符
        """

        self.chan.sendall('\n')

        while True:
            time.sleep(SLEEP_INTERVAL)
            res = self.chan.recv(RECV_BUFLEN)
            self.log(res, 'debug')
            buff = inspector.clear(res)
            if inspector.is_console_ready(buff):
                self.log(u'get_prompt success', 'debug')
                prompt = LINE_BREAK_RE.split(res)[-1]
                break
        return prompt

    def set_prompt(self, cmd=None):
        """
        尝试设置新的终端提示符
        """

        self.log(u'set_prompt: send enter', 'info')
        if cmd is None:
            cmd = self.set_proxy_prompt

        self.chan.sendall(cmd + '\n')
        while True:
            time.sleep(0.3)
            res = self.chan.recv(RECV_BUFLEN)
            self.log(res, 'debug')
            buff = inspector.clear(res)
            if buff.find("BKproxy") != -1:
                self.log(u'set_prompt success', 'debug')
                break

    @staticmethod
    def safe_close(ssh_or_chan):
        """
        安全关闭ssh连接或会话
        """

        try:
            if ssh_or_chan:
                ssh_or_chan.close()
        except:
            pass
