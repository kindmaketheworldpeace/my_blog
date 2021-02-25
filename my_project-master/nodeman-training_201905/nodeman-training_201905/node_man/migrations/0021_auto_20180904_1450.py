# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0020_auto_20180831_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoststatus',
            name='is_auto',
            field=models.CharField(default=b'AUTO', max_length=45, verbose_name='\u662f\u5426\u6258\u7ba1', choices=[(b'AUTO', b'AUTO'), (b'UNAUTO', b'UNAUTO')]),
        ),
        migrations.AddField(
            model_name='processcontrolinfo',
            name='health_cmd',
            field=models.CharField(default='', max_length=128, verbose_name='\u8fdb\u7a0b\u5065\u5eb7\u68c0\u67e5\u547d\u4ee4'),
        ),
        migrations.AddField(
            model_name='processcontrolinfo',
            name='kill_cmd',
            field=models.CharField(default='', max_length=128, verbose_name='kill\u547d\u4ee4'),
        ),
        migrations.AddField(
            model_name='processcontrolinfo',
            name='version_cmd',
            field=models.CharField(default='', max_length=128, verbose_name='\u8fdb\u7a0b\u7248\u672c\u67e5\u8be2\u547d\u4ee4'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPGRADE_PROXY', b'UPGRADE_PROXY'), (b'UPGRADE_AGENT', b'UPGRADE_AGENT'), (b'UPGRADE_PAGENT', b'UPGRADE_PAGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_CONFIG', b'UPDATE_CONFIG'), (b'START_PLUGIN', b'START_PLUGIN'), (b'STOP_PLUGIN', b'STOP_PLUGIN'), (b'RELOAD_PLUGIN', b'RELOAD_PLUGIN'), (b'RESTART_PLUGIN', b'RESTART_PLUGIN'), (b'DELEGATE_PLUGIN', b'DELEGATE_PLUGIN'), (b'UNDELEGATE_PLUGIN', b'UNDELEGATE_PLUGIN'), (b'UPGRADE_PLUGIN', b'UPGRADE_PLUGIN'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO')]),
        ),
        migrations.AlterField(
            model_name='jobtask',
            name='step',
            field=models.CharField(default=b'INIT', max_length=45, choices=[(b'INIT', '\u4efb\u52a1\u521d\u59cb\u5316'), (b'SSH_LOGIN', '\u767b\u5f55\u76ee\u6807\u4e3b\u673a'), (b'INSTALL_DEP', '\u5b89\u88c5\u57fa\u7840\u4f9d\u8d56'), (b'DOWNLOAD_FILE', '\u4e0b\u8f7d\u5b89\u88c5\u5305'), (b'UPLOAD_FILE', '\u4e0a\u4f20\u5b89\u88c5\u5305'), (b'EXECUTE_SCRIPT', '\u6267\u884c\u5b89\u88c5\u811a\u672c'), (b'SCRIPT_DONE', '\u5b89\u88c5\u811a\u672c\u6267\u884c\u5b8c\u6bd5'), (b'REGISTER_CMDB', '\u6ce8\u518c\u4e3b\u673a\u5230CMDB'), (b'WAIT_AGENT', '\u68c0\u6d4bAgent\u72b6\u6001\u548c\u7248\u672c'), (b'CREATE_JOB_SCRIPT', '\u51c6\u5907\u5b89\u88c5\u811a\u672c'), (b'CREATE_UNINSTALL_SCRIPT', '\u51c6\u5907\u5378\u8f7d\u811a\u672c'), (b'EXECUTE_JOB', '\u6267\u884c\u6279\u91cf\u5b89\u88c5\u4f5c\u4e1a'), (b'EXECUTE_UNINSTALL_JOB', '\u6267\u884c\u6279\u91cf\u5378\u8f7d\u4f5c\u4e1a'), (b'DETECT_WIN_ARC', '\u68c0\u6d4bWindows\u7cfb\u7edf\u7248\u672c'), (b'OVER_SUCCESS', '\u4efb\u52a1\u6267\u884c\u6210\u529f'), (b'OVER_FAILED', '\u4efb\u52a1\u6267\u884c\u5931\u8d25'), (b'REGISTER_PROCESS', '\u6ce8\u518c\u8fdb\u7a0b'), (b'OPERATE_PROCESS', '\u64cd\u4f5c\u8fdb\u7a0b')]),
        ),
    ]
