# -*- coding: utf-8 -*-
from celery import task
from change_task.models import (ScriptInstance)
from common.log import logger
import time

"""
异步任务
"""


@task()
def get_job_log(client, task_id, job_instance_list=[]):
    # 延迟10s查询
    time.sleep(10)
    # 针对每个业务获取执行结果
    for instance_kwargs in job_instance_list:
        get_job_result = client.job.get_job_instance_log(instance_kwargs)
        # 单个业务执行结果判断
        if get_job_result["result"]:
            job_data = get_job_result["data"][0]
            # 判断作业执行是否完成
            if job_data["is_finished"]:
                db_kwargs = {
                    "bk_biz_id": instance_kwargs["bk_biz_id"],
                    "job_instance_name": job_data["name"],
                    "job_instance_id": instance_kwargs["job_instance_id"],
                    "status": job_data["status"],
                    "is_finished": job_data["is_finished"],
                    "plain_results": job_data["step_results"],
                    "format_results": job_data["step_results"],
                    "job_instance_type": "CUSTOM",
                    "custom_task_id": task_id
                }
                try:
                    # 创建数据库记录，业务列表删除读取过业务
                    ScriptInstance.objects.create(**db_kwargs)
                    job_instance_list.remove(instance_kwargs)
                except Exception as e:
                    logger.exception(e)
            else:
                continue
    if job_instance_list:
        # 递归查询
        return get_job_log(client, task_id, job_instance_list)