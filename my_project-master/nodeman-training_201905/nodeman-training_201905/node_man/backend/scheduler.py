# -*- coding: utf-8 -*-

"""
celery任务入口
测试方法：设置celery_always_eager=True后启动测试，查看任务日志
遇到问题：测试中django创建的数据库，无法再celery中访问
"""
import datetime
from django.db.models import Min
from celery.task import task, periodic_task
from celery.schedules import crontab
from requests_tracker.models import Record, Exclude

from common.log import logger
from node_man.constants import JobType, StepType, PROC_STATUS_DICT, StatusType, CodeType
from node_man.models import Job, Host, JobTask, HostStatus, KV
from node_man.backend.tasks import (
    install_proxy, install_pagent,
    uninstall_agent
)
from node_man.backend.periodic_tasks import get_agent_status_task, clean_expired_info
from node_man.component.cmdb import GSEAgentApiModel, Business


@task
def installer(job_id, **kwargs):
    """
    按平台分组启动的celery任务，负责激活流程任务
    """

    logger.warning('%s: %s' % (Job.objects.values_list('pk'), job_id))

    job = Job.objects.get(id=job_id)
    job_tasks = job.get_job_tasks()
    time_limit = KV.get_timeout_config()

    # 安装proxy/agent
    if job.job_type in [
        JobType.INSTALL_PROXY,
        JobType.UPGRADE_PROXY,
        JobType.REINSTALL_PROXY,
        JobType.INSTALL_AGENT,
        JobType.UPGRADE_AGENT,
        JobType.REINSTALL_AGENT
    ]:
        for job_task in job_tasks:
            celery_task = install_proxy.apply_async(args=(job_task.pk,), kwargs=kwargs, soft_time_limit=time_limit)
            job_task.update_task_id(str(celery_task.task_id))
        return True

    # 安装pagent
    if job.job_type in [
        JobType.INSTALL_PAGENT,
        JobType.UPGRADE_PAGENT,
        JobType.REINSTALL_PAGENT]:
        celery_task = install_pagent.apply_async(args=(job_id,), kwargs=kwargs)
        job.update_task_id(str(celery_task.task_id))
        return True

    # 卸载proxy/agent
    if job.job_type in [JobType.UNINSTALL_AGENT, JobType.REMOVE_AGENT]:

        # 卸载 + 移除主机
        if job.job_type == JobType.REMOVE_AGENT:
            kwargs.update(need_remove=True)

        celery_task = uninstall_agent.apply_async(args=(job_id,), kwargs=kwargs)
        job.update_task_id(str(celery_task.task_id))
        return True

    raise NotImplementedError(u'暂不支持该任务类型：job_type = %s，请联系我们.' % job.job_type)
