# -*- coding: utf-8 -*-
"""
信号处理
"""
import django.dispatch

from common.log import logger

from node_man.models import TaskLog, Job, Host, JobTask
from node_man.utils.basic import now
from node_man import constants as const


class IpSignal(object):
    """
    Ip级别信号处理
    """

    def __init__(self, sender, job_id, username=None):
        self.sender = sender
        self.username = username if username is not None else ''
        self.job_id = job_id
        self.ip_id = ''
        self.target = {}

    def setup_ip(self, ip_id):
        self.ip_id = ip_id
        self.target = Host.objects.get(id=ip_id).__dict__
        return self

    def _log(self, content, level):
        if callable(getattr(logger, level, None)):
            getattr(logger, level)(content)

    def log(self, content, level='user'):
        signal_log.send(sender=self.sender, target=self.target, job_id=self.job_id,
                        level=level, content=content)
        self._log(content, level)
        return self

    def update_ip_status(self, status):
        signal_ip.send(sender=self.sender, job_id=self.job_id, ip_id=self.ip_id, status=status)
        return self

    def update_ip_code(self, err_code):
        signal_ip.send(sender=self.sender, job_id=self.job_id, ip_id=self.ip_id, err_code=err_code)
        return self

    def update_ip(self, status, err_code, desc=''):
        signal_ip.send(sender=self.sender, job_id=self.job_id, ip_id=self.ip_id,
                       status=status, err_code=err_code, desc=desc)
        return self


class JobSignal(object):
    """
    Job级别信号处理
    """

    def __init__(self, sender, job_id):
        self.sender = sender
        self.job_id = job_id
        self.username = Job.objects.get(id=job_id).username

    def _log(self, content, level):
        if callable(getattr(logger, level, None)):
            getattr(logger, level)(content)

    # 发送日志信号
    def log(self, content, level='user'):
        """
        级别日志: info/warning/error
        """

        content = u'<%s>: %s' % (self.job_id, content)
        signal_job.send(sender='install_agent', job_id=self.job_id, level=level, content=content)
        self._log(content, level)

        return self


# 定义并注册各个信号的处理函数
signal_job = django.dispatch.Signal(providing_args=['job_id', 'level', 'content'])


def job_handler(sender, job_id, level, content, **kwargs):
    """
    日志处理服务
    """

    try:
        job = Job.objects.get(id=job_id)
        log_item = TaskLog.objects.create(
            level=level,
            content=content
        )
        job.log.add(log_item)
        job.save()
    except Exception as e:
        logger.error(u'job_handler(Exception)【job_id=%s, content=%s】: %s' % (job_id, content, e))


signal_job.connect(job_handler, dispatch_uid='miya.handler.job_handler')

signal_log = django.dispatch.Signal(providing_args=['target', 'ip_id', 'job_id', 'level', 'content'])


def log_handler(sender, target, job_id, level, content, **kwargs):
    """
    日志处理服务
    """

    try:
        TaskLog.objects.create(
            inner_ip=target.get('inner_ip'),
            outer_ip=target.get('outer_ip'),
            biz_id=target.get('biz_id'),
            plat_id=target.get('plat_id'),
            task_id=job_id,
            level=level,
            content=content
        )
    except Exception as e:
        logger.error(u'log_handler(Exception)【target=%s, job_id=%s, content=%s】: %s' % (target, job_id, content, e))


signal_log.connect(log_handler, dispatch_uid='miya.handler.log_handler')

signal_ip = django.dispatch.Signal(providing_args=['job_id', 'ip_id', 'status', 'err_code', 'desc'])


def ip_handler(sender, job_id, ip_id, status=None, err_code=None, desc='', **kwargs):
    """
    IP状态更新服务
    """

    try:
        ip = Host.objects.get(id=ip_id)
        ip_job = JobTask.objects.get(ip_id=ip_id, job_id=job_id)
    except Host.DoesNotExist:
        logger.error(u'ip does not exist: ip_id=%s' % ip_id)
    except JobTask.DoesNotExist:
        logger.error(u'ip_job does not exist: ip_id=%s, job_id=%s' % (ip_id, job_id))
    else:
        # 状态更新
        if status is not None:
            ip.status = status
            ip_job.task_status = status
            # 结束时间记录，同时更新历史任务单据IpJob记录
            if status in [const.StatusType.success, const.StatusType.failed]:
                ip_job.end_time = now()
                ip.end_time = now()
                ip_job.desc = desc
                ip.desc = desc

        # 错误码更新
        if err_code is not None:
            ip_job.err_code = err_code
            ip.err_code = err_code
            ip_job.desc = desc
            ip.desc = desc

        ip.save()
        ip_job.save()


signal_ip.connect(ip_handler, dispatch_uid='miya.handler.ip_handler')
