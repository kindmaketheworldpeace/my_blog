# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0011_auto_20180525_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobtask',
            name='err_code',
            field=models.CharField(default=b'INIT', max_length=45, choices=[(b'INIT', b'INIT'), (b'SUCCESS', b'SUCCESS'), (b'STILL_RUNNING', b'STILL_RUNNING'), (b'CELERY_TASK_EXCEPT', b'CELERY_TASK_EXCEPT'), (b'CELERY_TASK_TIMEOUT', b'CELERY_TASK_TIMEOUT'), (b'WAIT_AGENT_TIMEOUT', b'WAIT_AGENT_TIMEOUT'), (b'UNEXPECTED_RETURN', b'UNEXPECTED_RETURN'), (b'CURL_FILE_FAILED', b'CURL_FILE_FAILED'), (b'REGISTER_FAILED', b'REGISTER_FAILED'), (b'START_JOB_FAILED', b'START_JOB_FAILED'), (b'JOB_TIMEOUT', b'JOB_TIMEOUT'), (b'WAIT_AGENT_FAILED', b'WAIT_AGENT_FAILED'), (b'IJOBS_FAILED', b'IJOBS_FAILED'), (b'FORCE_STOP', b'FORCE_STOP'), (b'INSTALL_FAILED', b'INSTALL_FAILED'), (b'SSH_LOGIN_TIMEOUT', b'SSH_LOGIN_TIMEOUT'), (b'SSH_WRONG_PASSWORD', b'SSH_WRONG_PASSWORD'), (b'SSH_LOGIN_EXCEPT', b'SSH_LOGIN_EXCEPT'), (b'SSH_LOGIN_KEY_ERR', b'SSH_LOGIN_KEY_ERR'), (b'NOT_SUPPORT_AUTH_WAY', b'NOT_SUPPORT_AUTH_WAY'), (b'SOCKET_TIMEOUT', b'SOCKET_TIMEOUT'), (b'UPLOAD_FAILED', b'UPLOAD_FAILED'), (b'DETECT_ARC_FAILED', b'DETECT_ARC_FAILED'), (b'COMMAND_NOT_FOUND', b'COMMAND_NOT_FOUND'), (b'FILE_DOES_NOT_EXIST', b'FILE_DOES_NOT_EXIST')]),
        ),
    ]
