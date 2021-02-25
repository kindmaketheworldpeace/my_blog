# -*- coding: utf-8 -*-

import inspect

from django.contrib import admin

from . import models

# 自动导入所有model
for name, obj in inspect.getmembers(models):
    try:
        if inspect.isclass(obj) and name not in [
            "HostStatus", "Job", "Host",
            "IP", "SshKey", "JobTask",
            "TaskLog"
        ]:
            admin.site.register(getattr(models, name))
    except Exception as e:
        pass


class JobAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'creator', 'job_type',
        'start_time', 'end_time', 'task_id', 'is_canceled')
    search_fields = ['job_type']
    list_filter = ["job_type"]


class JobTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'job', 'host', 'status',
        'err_code', 'err_desc', 'task_id',
        'step', 'step_index', 'create_time', 'end_time')
    search_fields = ['job__id']
    list_filter = ["job__id"]


class HostAdmin(admin.ModelAdmin):
    list_display = (
        'inner_ip', 'bk_cloud_id', 'bk_biz_id', 'node_type',
        'is_deleted', 'update_time')
    search_fields = ['inner_ip']
    list_filter = ["agent_status", "is_deleted"]


class HostStatusAdmin(admin.ModelAdmin):
    list_display = (
        'host', 'name', 'status', 'is_auto', 'version', 'proc_type')
    search_fields = ['host', 'name']
    list_filter = ["status", "is_auto"]


class TaskLogAdmin(admin.ModelAdmin):
    list_display = (
        'level', 'content', 'flag',
        'create_time', 'job_task_id', 'job_id')
    search_fields = ['job_id', 'job_task_id']
    list_filter = ["job_id", "job_task_id"]


admin.site.register(models.HostStatus, HostStatusAdmin)
admin.site.register(models.Job, JobAdmin)
admin.site.register(models.JobTask, JobTaskAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.TaskLog, TaskLogAdmin)
