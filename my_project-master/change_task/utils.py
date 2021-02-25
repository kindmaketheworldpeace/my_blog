# -*- coding: utf-8 -*-
"""
系统管理工具包
"""
from change_task.tasks.async_tasks import get_job_log
from component.constants import ResponseCodeStatus
from operator import itemgetter
from itertools import groupby
import base64
from blueking.component.shortcuts import get_client_by_user
from change_task.models import (SceneTask, CustomTask)


def run_task_instance(user, task_id, task_type):
    """
    :param user: 启动任务的用户名
    :param task_id: 任务ID
    :param task_type: 任务类型，1为自定义任务，0为场景任务
    :return: result 任务执行结果

    """

    client = get_client_by_user(user)

    task_instance = CustomTask.objects.get(id=task_id) if task_type else SceneTask.objects.get(id=task_id)
    # 修改任务状态
    task_instance.status = 2
    task_instance.save()
    kwargs = {
        "bk_biz_id": "",
        "script_content": base64.b64encode(task_instance.script_content),
        "script_param": base64.b64encode(task_instance.script_param),
        "script_timeout": task_instance.script_timeout,
        "account": task_instance.account,
        "is_param_sensitive": 1,
        "script_type": task_instance.script_type,
        "ip_list": [],
    }
    job_instance_list = []
    ip_list = eval(task_instance.ip_list)
    ip_list.sort(key=itemgetter('bk_biz_id'))
    # 对不同业务的IP进行分组
    ip_list_group = groupby(ip_list, itemgetter('bk_biz_id'))

    for biz_id, ips in ip_list_group:
        kwargs["bk_biz_id"] = int(biz_id)
        kwargs["ip_list"] = list(ips)
        # 分业务调用脚本执行接口
        job_exec_result = client.job.fast_execute_script(kwargs)
        if job_exec_result["result"]:
            job_instance_list.append({
                "bk_biz_id": int(biz_id),
                "job_instance_id": job_exec_result["data"]["job_instance_id"]})
        else:
            task_instance.status = 4
            task_instance.save()
    get_job_log.apply_async(client, task_id, job_instance_list)
    return {'result': True, 'code': ResponseCodeStatus.OK, 'message': 'success', 'data': None}
