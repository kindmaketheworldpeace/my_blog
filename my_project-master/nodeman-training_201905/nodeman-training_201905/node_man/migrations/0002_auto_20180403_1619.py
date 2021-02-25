# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='agent_status',
            field=models.IntegerField(default=0, verbose_name='agent\u8fd0\u884c\u72b6\u6001', choices=[(b'1', b'RUNNING'), (b'0', b'UNKNOWN'), (b'2', b'TERMINATED')]),
        ),
        migrations.AddField(
            model_name='host',
            name='job_status',
            field=models.IntegerField(default=0, verbose_name='\u4f5c\u4e1a\u72b6\u6001', choices=[(0, b'QUEUE'), (1, b'RUNNING'), (2, b'SUCCESS'), (3, b'FAILED')]),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_CONFIG', b'UPDATE_CONFIG'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO')]),
        ),
        migrations.AlterField(
            model_name='jobtask',
            name='err_code',
            field=models.CharField(default=b'INIT', max_length=45, choices=[(b'INIT', b'INIT'), (b'SUCCESS', b'SUCCESS'), (b'STILL_RUNNING', b'STILL_RUNNING'), (b'CELERY_TASK_EXCEPT', b'CELERY_TASK_EXCEPT'), (b'CELERY_TASK_TIMEOUT', b'CELERY_TASK_TIMEOUT'), (b'WAIT_AGENT_TIMEOUT', b'WAIT_AGENT_TIMEOUT'), (b'UNEXPECTED_RETURN', b'UNEXPECTED_RETURN'), (b'CURL_FILE_FAILED', b'CURL_FILE_FAILED'), (b'REGISTER_FAILED', b'REGISTER_FAILED'), (b'START_JOB_FAILED', b'START_JOB_FAILED'), (b'JOB_TIMEOUT', b'JOB_TIMEOUT'), (b'WAIT_AGENT_FAILED', b'WAIT_AGENT_FAILED'), (b'IJOBS_FAILED', b'IJOBS_FAILED'), (b'FORCE_STOP', b'FORCE_STOP'), (b'INSTALL_FAILED', b'INSTALL_FAILED'), (b'SSH_LOGIN_TIMEOUT', b'SSH_LOGIN_TIMEOUT'), (b'SSH_WRONG_PASSWORD', b'SSH_WRONG_PASSWORD'), (b'SSH_LOGIN_EXCEPT', b'SSH_LOGIN_EXCEPT'), (b'SSH_LOGIN_KEY_ERR', b'SSH_LOGIN_KEY_ERR'), (b'NOT_SUPPORT_AUTH_WAY', b'NOT_SUPPORT_AUTH_WAY'), (b'SOCKET_TIMEOUT', b'SOCKET_TIMEOUT'), (b'UPLOAD_FAILED', b'UPLOAD_FAILED'), (b'DETECT_ARC_FAILED', b'DETECT_ARC_FAILED'), (b'COMMAND_NOT_FOUND', b'COMMAND_NOT_FOUND')]),
        ),
        migrations.AlterField(
            model_name='jobtask',
            name='step',
            field=models.CharField(default=b'INIT', max_length=45, choices=[(b'INIT', '\u4efb\u52a1\u521d\u59cb\u5316'), (b'SSH_LOGIN', '\u767b\u5f55\u76ee\u6807\u4e3b\u673a'), (b'INSTALL_DEP', '\u5b89\u88c5\u57fa\u7840\u4f9d\u8d56'), (b'DOWNLOAD_FILE', '\u4e0b\u8f7d\u5b89\u88c5\u5305'), (b'UPLOAD_FILE', '\u4e0a\u4f20\u5b89\u88c5\u5305'), (b'EXECUTE_SCRIPT', '\u6267\u884c\u5b89\u88c5\u811a\u672c'), (b'SCRIPT_DONE', '\u5b89\u88c5\u811a\u672c\u6267\u884c\u5b8c\u6bd5'), (b'REGISTER_CMDB', '\u6ce8\u518c\u4e3b\u673a\u5230CMDB'), (b'WAIT_AGENT', '\u7b49\u5f85Agent\u8fde\u63a5\u5c31\u7eea'), (b'CREATE_JOB_SCRIPT', '\u51c6\u5907\u5b89\u88c5\u811a\u672c'), (b'EXECUTE_JOB', '\u6267\u884c\u6279\u91cf\u5b89\u88c5\u4f5c\u4e1a'), (b'DETECT_WIN_ARC', '\u68c0\u6d4bWindows\u7cfb\u7edf\u7248\u672c'), (b'OVER_SUCCESS', '\u5b89\u88c5\u6210\u529f'), (b'OVER_FAILED', '\u5b89\u88c5\u5931\u8d25')]),
        ),
    ]
