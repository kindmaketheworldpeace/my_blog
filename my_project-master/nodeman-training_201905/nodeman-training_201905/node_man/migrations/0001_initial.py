# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20180306_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cloud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_cloud_id', models.CharField(unique=True, max_length=45)),
                ('bk_cloud_name', models.CharField(unique=True, max_length=45)),
                ('bk_supplier_id', models.CharField(max_length=45)),
                ('creator', models.CharField(max_length=45, null=True, blank=True)),
                ('bk_biz_id', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e91\u533a\u57df\u4fe1\u606f',
                'verbose_name_plural': '\u4e91\u533a\u57df\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bk_biz_id', models.CharField(max_length=45)),
                ('bk_cloud_id', models.CharField(max_length=45, verbose_name='\u5e73\u53f0ID')),
                ('inner_ip', models.CharField(max_length=45, verbose_name='\u5185\u7f51IP')),
                ('outer_ip', models.CharField(max_length=45, null=True, verbose_name='\u5916\u7f51IP', blank=True)),
                ('os_type', models.CharField(default='linux', max_length=45, choices=[(b'WINDOWS', b'WINDOWS'), (b'LINUX', b'LINUX'), (b'AIX', b'AIX')])),
                ('node_type', models.CharField(max_length=45, verbose_name='\u8282\u70b9\u7c7b\u578b', choices=[(b'AGENT', b'AGENT'), (b'PROXY', b'PROXY'), (b'PAGENT', b'PAGENT')])),
                ('auth_type', models.CharField(default=b'PASSWORD', max_length=45, choices=[(b'PASSWORD', b'PASSWORD'), (b'KEY', b'KEY')])),
                ('account', models.CharField(default='', max_length=45, verbose_name='\u8d26\u6237\u540d')),
                ('password', models.CharField(max_length=45, null=True, verbose_name='\u5bc6\u7801', blank=True)),
                ('port', models.IntegerField(default=22, null=True, verbose_name='\u7aef\u53e3')),
                ('key', models.TextField(null=True, verbose_name='\u5bc6\u94a5\u5185\u5bb9', blank=True)),
                ('has_cygwin', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6709\u6548')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4fe1\u606f',
                'verbose_name_plural': '\u4e3b\u673a\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='HostStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='gseagent', max_length=45, verbose_name='\u8fdb\u7a0b\u540d\u79f0')),
                ('status', models.CharField(default=b'UNKNOWN', max_length=45, verbose_name='\u8fdb\u7a0b\u72b6\u6001', choices=[(b'RUNNING', b'RUNNING'), (b'UNKNOWN', b'UNKNOWN'), (b'TERMINATED', b'TERMINATED')])),
                ('version', models.CharField(default='', max_length=45, null=True, verbose_name='\u8fdb\u7a0b\u7248\u672c', blank=True)),
                ('proc_type', models.CharField(default=b'AGENT', max_length=45, verbose_name='\u8fdb\u7a0b\u7c7b\u578b', choices=[(b'AGENT', b'AGENT'), (b'PLUGIN', b'PLUGIN')])),
                ('host', models.ForeignKey(related_name='status', blank=True, to='node_man.Host', null=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u72b6\u6001',
                'verbose_name_plural': '\u4e3b\u673a\u72b6\u6001',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.CharField(default='', max_length=45, verbose_name='\u64cd\u4f5c\u4eba')),
                ('bk_biz_id', models.CharField(max_length=45, verbose_name='\u4e1a\u52a1ID')),
                ('bk_cloud_id', models.CharField(max_length=45, verbose_name='\u533a\u57dfID')),
                ('job_type', models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_CONFIG', b'UPDATE_CONFIG')])),
                ('start_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u4efb\u52a1\u65f6\u95f4')),
                ('end_time', models.DateTimeField(null=True, verbose_name='\u4efb\u52a1\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('task_id', models.CharField(max_length=32, null=True, verbose_name='\u5173\u8054\u7684celery_id', blank=True)),
                ('bk_job_id', models.CharField(max_length=32, null=True, verbose_name='\u5173\u8054\u7684job_id', blank=True)),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u4fe1\u606f',
                'verbose_name_plural': '\u4efb\u52a1\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='JobTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'QUEUE', max_length=45, choices=[(b'QUEUE', b'QUEUE'), (b'RUNNING', b'RUNNING'), (b'SUCCESS', b'SUCCESS'), (b'FAILED', b'FAILED')])),
                ('err_code', models.CharField(default=b'INIT', max_length=45, choices=[(b'INIT', b'INIT'), (b'SUCCESS', b'SUCCESS'), (b'STILL_RUNNING', b'STILL_RUNNING'), (b'CELERY_TASK_EXCEPT', b'CELERY_TASK_EXCEPT'), (b'CELERY_TASK_TIMEOUT', b'CELERY_TASK_TIMEOUT'), (b'WAIT_AGENT_TIMEOUT', b'WAIT_AGENT_TIMEOUT'), (b'UNEXPECTED_RETURN', b'UNEXPECTED_RETURN'), (b'CURL_FILE_FAILED', b'CURL_FILE_FAILED'), (b'REGISTER_FAILED', b'REGISTER_FAILED'), (b'START_JOB_FAILED', b'START_JOB_FAILED'), (b'JOB_TIMEOUT', b'JOB_TIMEOUT'), (b'IJOBS_FAILED', b'IJOBS_FAILED'), (b'FORCE_STOP', b'FORCE_STOP'), (b'INSTALL_FAILED', b'INSTALL_FAILED'), (b'SSH_LOGIN_TIMEOUT', b'SSH_LOGIN_TIMEOUT'), (b'SSH_WRONG_PASSWORD', b'SSH_WRONG_PASSWORD'), (b'SSH_LOGIN_EXCEPT', b'SSH_LOGIN_EXCEPT'), (b'SSH_LOGIN_KEY_ERR', b'SSH_LOGIN_KEY_ERR'), (b'NOT_SUPPORT_AUTH_WAY', b'NOT_SUPPORT_AUTH_WAY'), (b'SOCKET_TIMEOUT', b'SOCKET_TIMEOUT'), (b'COMMAND_NOT_FOUND', b'COMMAND_NOT_FOUND')])),
                ('err_desc', models.CharField(default='', max_length=255)),
                ('task_id', models.CharField(max_length=45, null=True, verbose_name='\u5bf9\u5e94\u7684celery\u4efb\u52a1id', blank=True)),
                ('step', models.CharField(default=b'INIT', max_length=45, choices=[(b'INIT', '\u4efb\u52a1\u521d\u59cb\u5316'), (b'SSH_LOGIN', '\u767b\u5f55\u76ee\u6807\u4e3b\u673a'), (b'INSTALL_DEP', '\u5b89\u88c5\u57fa\u7840\u4f9d\u8d56'), (b'DOWNLOAD_FILE', '\u4e0b\u8f7d\u5b89\u88c5\u5305'), (b'EXECUTE_SCRIPT', '\u6267\u884c\u5b89\u88c5\u811a\u672c'), (b'SCRIPT_DONE', '\u5b89\u88c5\u811a\u672c\u6267\u884c\u5b8c\u6bd5'), (b'REGISTER_CMDB', '\u6ce8\u518c\u4e3b\u673a\u5230CMDB'), (b'WAIT_AGENT', '\u7b49\u5f85Agent\u8fde\u63a5\u5c31\u7eea'), (b'CREATE_JOB_SCRIPT', '\u51c6\u5907\u5b89\u88c5\u811a\u672c'), (b'EXECUTE_JOB', '\u6267\u884c\u6279\u91cf\u5b89\u88c5\u4f5c\u4e1a'), (b'OVER_SUCCESS', '\u5b89\u88c5\u6210\u529f'), (b'OVER_FAILED', '\u5b89\u88c5\u5931\u8d25')])),
                ('step_index', models.IntegerField(default=0, verbose_name='\u6b65\u9aa4\u5e8f\u53f7')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('host', models.ForeignKey(related_name='job_result', to='node_man.Host', help_text='\u5bf9\u5e94\u7684\u4e3b\u673a\u4fe1\u606f')),
                ('job', models.ForeignKey(related_name='hosts', to='node_man.Job', help_text='\u5bf9\u5e94\u7684\u4f5c\u4e1a\u4fe1\u606f')),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u8be6\u60c5',
                'verbose_name_plural': '\u4efb\u52a1\u8be6\u60c5',
            },
        ),
        migrations.CreateModel(
            name='KV',
            fields=[
                ('key', models.CharField(max_length=255, serialize=False, verbose_name='\u952e', primary_key=True, db_index=True)),
                ('v_json', jsonfield.fields.JSONField(verbose_name='\u503c')),
            ],
            options={
                'verbose_name': '\u914d\u7f6e\u8868',
                'verbose_name_plural': '\u914d\u7f6e\u8868',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('bk_token', models.CharField(max_length=45)),
                ('bk_user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, help_text='\u5173\u8054\u7528\u6237')),
                ('favorite', jsonfield.fields.JSONField(verbose_name='\u7528\u6237\u6536\u85cf\u4fe1\u606f\uff0c\u6bd4\u5982\u4e91\u533a\u57df\u7b49')),
            ],
            options={
                'verbose_name': '\u4e2a\u4eba\u8d44\u6599',
                'verbose_name_plural': '\u4e2a\u4eba\u8d44\u6599',
            },
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(default=b'USER', max_length=45, choices=[(b'USER', b'USER'), (b'WARNING', b'WARNING'), (b'ERROR', b'ERROR')])),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('job_task_id', models.IntegerField(null=True, verbose_name='\u5173\u8054\u7684JobTask', blank=True)),
                ('job_id', models.IntegerField(null=True, verbose_name='\u5173\u8054\u7684Job', blank=True)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '\u4efb\u52a1\u65e5\u5fd7',
                'verbose_name_plural': '\u4efb\u52a1\u65e5\u5fd7',
            },
        ),
    ]
