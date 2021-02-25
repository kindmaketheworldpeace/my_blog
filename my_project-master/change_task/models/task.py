# -*- coding: utf-8 -*-

import jsonfield
from django.db import models

from component.constants import (
    LEN_SHORT,
    LEN_NORMAL,
    LEN_MIDDLE,
    LEN_X_LONG,
    EMPTY_LIST,
    EMPTY_DICT,
    ROLE_CHOICES,
    SCRIPT_CHOICES,
    TASK_STATUS_CHOICES,
    JOB_STATUS_CHOICES,
)
from change_task.models.basic import Model
from change_task.managers import Manager


class Scene(Model):
    OS_CHOICES = [
        ("LINUX", u"linux"),
        ("WINDOWS", u"windows"),
    ]

    name = models.CharField(u"场景名称", max_length=LEN_NORMAL)
    description = models.TextField(u"描述信息", blank=True)
    # 前后通过逗号隔开，ex: ,kris,
    display_role = models.CharField(u"可见范围", max_length=LEN_X_LONG, blank=True)
    display_type = models.CharField(u"可见范围类型", max_length=LEN_SHORT, choices=ROLE_CHOICES, default="OPEN")
    account = models.CharField(u"服务器帐户", max_length=LEN_SHORT)
    os_type = models.CharField(u"操作系统类型", max_length=LEN_SHORT, choices=OS_CHOICES)
    script_type = models.IntegerField(u"脚本来源", choices=SCRIPT_CHOICES)
    # 输入参数按顺序对应的显示名称
    input_display_list = jsonfield.JSONField(u"脚本参数显示名", default=EMPTY_LIST)
    # [{"key": "result", display": "是否成功"}, ]
    output_display_map = jsonfield.JSONField(u"脚本结果显示名映射", default=EMPTY_DICT)
    script_content = models.TextField(u"脚本内容", blank=True)
    # 脚本超时时间，秒。取值范围60-86400
    script_timeout = models.IntegerField(u"超时时间(s)", default=1000)
    is_use = models.BooleanField(u"是否启用", default=True)
    objects = Manager()

    class Meta:
        verbose_name = u"场景"
        verbose_name_plural = u"场景"
        ordering = ("-id",)

    def __unicode__(self):
        return "%s" % self.name


class SceneTask(Model):
    name = models.CharField(u"场景任务名称", max_length=LEN_NORMAL)
    serivce_privider = models.CharField(u"服务商", max_length=LEN_SHORT)
    account = models.CharField(u"服务器帐户", max_length=LEN_SHORT)
    # 业务ID列表 ex: [2, 3]
    biz_list = jsonfield.JSONField(u"业务", default=EMPTY_LIST)
    """
    "ip_list": [
        {
            "bk_biz_id": 2,
            "bk_cloud_id": 0,
            "ip": "10.0.0.1",
            "alived": 1 # Agent正常
        },
    ]
    """
    ip_list = jsonfield.JSONField(u"目标机器", default=EMPTY_LIST)
    script_type = models.IntegerField(u"脚本来源", choices=SCRIPT_CHOICES)
    # 输入参数按顺序对应的显示名称
    input_display_list = jsonfield.JSONField(u"脚本参数显示名", default=EMPTY_LIST)
    # 以空格隔开的字符串
    script_param = models.CharField(u"脚本参数", max_length=LEN_MIDDLE)
    # [{"key": "result", display": "是否成功"}, ]
    output_display_map = jsonfield.JSONField(u"脚本结果显示名映射", default=EMPTY_DICT)
    script_content = models.TextField(u"脚本内容", blank=True)
    # 脚本超时时间，秒。取值范围60-86400
    script_timeout = models.IntegerField(u"超时时间(s)", default=1000)
    status = models.IntegerField(u"任务状态", choices=TASK_STATUS_CHOICES)
    """
    {
        "name": "规则一",
        "result": "REJECT", # (拒绝)规则结果
        "condition": {
            "expressions": [
                {
                    "expressions": [
                        {
                            "key": "time",
                            "condition": "in",
                            "value": ["9:00", "21:00"]
                        }
                    ],
                    "type": "and" # (且)单个条件组内的条件关系
                }
            ],
            "type": "or" # (或)条件组之间关系
        }
    }
    """
    rule_info = jsonfield.JSONField(u"应用规则详情", default=EMPTY_DICT)
    scene = models.ForeignKey(Scene, help_text=u"场景", related_name="tasks", on_delete=models.SET_NULL, null=True,
                              blank=True)

    objects = Manager()

    class Meta:
        verbose_name = u"场景任务"
        verbose_name_plural = u"场景任务"

    def __unicode__(self):
        return "%s(%s)" % (self.name, self.serivce_privider)


class CustomTask(Model):
    name = models.CharField(u"自定义任务名称", max_length=LEN_NORMAL)
    serivce_privider = models.CharField(u"服务商", max_length=LEN_SHORT)
    account = models.CharField(u"服务器帐户", max_length=LEN_SHORT)
    # 业务ID列表 ex: [2, 3]
    biz_list = jsonfield.JSONField(u"业务", default=EMPTY_LIST)
    """
    "ip_list": [
        {
            "bk_biz_id": 2,
            "bk_cloud_id": 0,
            "ip": "10.0.0.1",
            "alived": 1 # Agent正常
        },
    ]
    """
    ip_list = jsonfield.JSONField(u"目标机器", default=EMPTY_LIST)
    script_type = models.IntegerField(u"脚本来源", choices=SCRIPT_CHOICES)
    # 以空格隔开的字符串
    script_param = models.CharField(u"脚本参数", max_length=LEN_MIDDLE)
    script_content = models.TextField(u"脚本内容", blank=True)
    # 脚本超时时间，秒。取值范围60-86400
    script_timeout = models.IntegerField(u"超时时间(s)", default=1000)
    status = models.IntegerField(u"任务状态", choices=TASK_STATUS_CHOICES)
    """
    {
        "name": "规则一",
        "result": "REJECT", # (拒绝)规则结果
        "condition": {
            "expressions": [
                {
                    "expressions": [
                        {
                            "key": "time",
                            "condition": "in",
                            "value": ["9:00", "21:00"]
                        }
                    ],
                    "type": "and" # (且)单个条件组内的条件关系
                }
            ],
            "type": "or" # (或)条件组之间关系
        }
    }
    """
    rule_info = jsonfield.JSONField(u"应用规则详情", default=EMPTY_DICT)

    objects = Manager()

    class Meta:
        verbose_name = u"自定义任务"
        verbose_name_plural = u"自定义任务"

    def __unicode__(self):
        return "%s(%s)" % (self.name, self.serivce_privider)


class ScriptInstance(Model):
    INSTANCE_TYPE_CHOICES = [
        ("CUSTOM", u"自定义"),
        ("SCENE", u"场景"),
    ]

    bk_biz_id = models.IntegerField(u"业务ID")
    job_instance_name = models.CharField(u"脚本实例名称", max_length=LEN_NORMAL)
    job_instance_id = models.IntegerField(u"脚本实例ID")
    status = models.IntegerField(u"脚本实例状态", choices=JOB_STATUS_CHOICES)
    is_finished = models.BooleanField(u"脚本实例是否结束", default=False)
    job_instance_type = models.CharField(u"脚本实例类型", max_length=LEN_SHORT, choices=INSTANCE_TYPE_CHOICES)
    '''
    [
        {
            "ip_status": 9,
            "tag": "xxx",
            "ip_logs": [
                {
                    "retry_count": 0,
                    "total_time": 60.599,
                    "start_time": "2018-03-15 14:39:30 +0800",
                    "end_time": "2018-03-15 14:40:31 +0800",
                    "ip": "10.0.0.1",
                    "bk_cloud_id": 0,
                    "error_code": 0,
                    "exit_code": 0,
                    "log_content": "[2018-03-15 14:39:30][PID:56875] job_start\n"
                }
            ]
        }
    ]
    '''
    plain_results = jsonfield.JSONField(u"原始结果日志", default=EMPTY_LIST)
    '''
    # 以IP地址平铺出来的展示
    [
        {
            "retry_count": 0,
            "total_time": 60.599,
            "start_time": "2018-03-15 14:39:30 +0800",
            "end_time": "2018-03-15 14:40:31 +0800",
            "ip": "10.0.0.1",
            "bk_cloud_id": 0,
            "error_code": 0,
            "exit_code": 0,
            "ip_status": 9,
            # 场景任务类型
            "log_content": [
                {"key": "result", display": "是否成功", "value": "成功"},
                {"key": "detail", display": "详细信息", "value": "这是一段详情信息..."},
            ]
            # 自定义任务类型
            "log_content": "[2018-03-15 14:39:30][PID:56875] job_start\n"
        }
    ]
    '''
    format_results = jsonfield.JSONField(u"格式化结果日志", default=EMPTY_LIST)
    scene_task = models.ForeignKey(SceneTask, help_text=u"场景任务", related_name="scene_script_instances",
                                   blank=True, null=True)
    custom_task = models.ForeignKey(CustomTask, help_text=u"自定义任务", related_name="custom_script_instances",
                                    blank=True, null=True)

    objects = Manager()

    class Meta:
        verbose_name = u"脚本实例"
        verbose_name_plural = u"脚本实例"

    def __unicode__(self):
        return "%s(%s)" % (self.job_instance_name, self.job_instance_type)
