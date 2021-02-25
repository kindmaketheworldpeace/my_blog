# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0023_auto_20180918_1949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='processcontrolinfo',
            options={'verbose_name': '\u6a21\u5757/\u8fdb\u7a0b\u63a7\u5236\u4fe1\u606f\u8868', 'verbose_name_plural': '\u6a21\u5757/\u8fdb\u7a0b\u63a7\u5236\u4fe1\u606f\u8868'},
        ),
        migrations.RenameField(
            model_name='gseplugin',
            old_name='config_file_format',
            new_name='config_format',
        ),
        migrations.AddField(
            model_name='gseplugin',
            name='auto_launch',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5728\u6210\u529f\u5b89\u88c5agent\u540e\u81ea\u52a8\u62c9\u8d77'),
        ),
        migrations.AddField(
            model_name='processpackage',
            name='cpu_arc',
            field=models.CharField(default=b'x86_64', max_length=32, verbose_name='CPU\u7c7b\u578b', choices=[(b'x86', b'x86'), (b'x86_64', b'x86_64'), (b'powerpc', b'powerpc')]),
        ),
        migrations.AddField(
            model_name='processpackage',
            name='os',
            field=models.CharField(default=b'linux', max_length=32, verbose_name='\u7cfb\u7edf\u7c7b\u578b', choices=[(b'windows', b'windows'), (b'linux', b'linux'), (b'aix', b'aix')]),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPGRADE_PROXY', b'UPGRADE_PROXY'), (b'UPGRADE_AGENT', b'UPGRADE_AGENT'), (b'UPGRADE_PAGENT', b'UPGRADE_PAGENT'), (b'IMPORT_PROXY', b'IMPORT_PROXY'), (b'IMPORT_AGENT', b'IMPORT_AGENT'), (b'IMPORT_PAGENT', b'IMPORT_PAGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'START_PLUGIN', b'START_PLUGIN'), (b'STOP_PLUGIN', b'STOP_PLUGIN'), (b'RELOAD_PLUGIN', b'RELOAD_PLUGIN'), (b'RESTART_PLUGIN', b'RESTART_PLUGIN'), (b'DELEGATE_PLUGIN', b'DELEGATE_PLUGIN'), (b'UNDELEGATE_PLUGIN', b'UNDELEGATE_PLUGIN'), (b'UPGRADE_PLUGIN', b'UPGRADE_PLUGIN'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO')]),
        ),
        migrations.AlterField(
            model_name='jobtask',
            name='step',
            field=models.CharField(default=b'INIT', max_length=45, choices=[(b'REPLACE_CONFIG', '\u66ff\u6362\u914d\u7f6e'), (b'INIT', '\u4efb\u52a1\u521d\u59cb\u5316'), (b'SSH_LOGIN', '\u767b\u5f55\u76ee\u6807\u4e3b\u673a'), (b'INSTALL_DEP', '\u5b89\u88c5\u57fa\u7840\u4f9d\u8d56'), (b'DOWNLOAD_FILE', '\u4e0b\u8f7d\u5b89\u88c5\u5305'), (b'UPLOAD_FILE', '\u4e0a\u4f20\u5b89\u88c5\u5305'), (b'EXECUTE_SCRIPT', '\u6267\u884c\u5b89\u88c5\u811a\u672c'), (b'SCRIPT_DONE', '\u5b89\u88c5\u811a\u672c\u6267\u884c\u5b8c\u6bd5'), (b'REGISTER_CMDB', '\u6ce8\u518c\u4e3b\u673a\u5230CMDB'), (b'WAIT_AGENT', '\u68c0\u6d4bAgent\u72b6\u6001\u548c\u7248\u672c'), (b'CREATE_JOB_SCRIPT', '\u51c6\u5907\u5b89\u88c5\u811a\u672c'), (b'CREATE_UNINSTALL_SCRIPT', '\u51c6\u5907\u5378\u8f7d\u811a\u672c'), (b'EXECUTE_JOB', '\u6267\u884c\u6279\u91cf\u5b89\u88c5\u4f5c\u4e1a'), (b'EXECUTE_UNINSTALL_JOB', '\u6267\u884c\u6279\u91cf\u5378\u8f7d\u4f5c\u4e1a'), (b'DETECT_WIN_ARC', '\u68c0\u6d4bWindows\u7cfb\u7edf\u7248\u672c'), (b'OVER_SUCCESS', '\u4efb\u52a1\u6267\u884c\u6210\u529f'), (b'OVER_FAILED', '\u4efb\u52a1\u6267\u884c\u5931\u8d25'), (b'REGISTER_PROCESS', '\u6ce8\u518c\u8fdb\u7a0b'), (b'OPERATE_PROCESS', '\u64cd\u4f5c\u8fdb\u7a0b'), (b'UPLOAD_FILE', '\u4e0a\u4f20\u6587\u4ef6'), (b'OVERWRITE_FILE', '\u66ff\u6362\u6587\u4ef6'), (b'RESTART_PROCESS', '\u91cd\u542f\u8fdb\u7a0b'), (b'DELEGATE_PROCESS', '\u6258\u7ba1\u8fdb\u7a0b')]),
        ),
    ]
