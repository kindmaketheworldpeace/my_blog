# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0016_auto_20180822_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_CONFIG', b'UPDATE_CONFIG'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO'), (b'UPGRADE_PROXY', b'UPGRADE_PROXY'), (b'UPGRADE_AGENT', b'UPGRADE_AGENT'), (b'UPGRADE_PAGENT', b'UPGRADE_PAGENT'), (b'START_PLUGIN', b'START_PLUGIN'), (b'STOP_PLUGIN', b'STOP_PLUGIN'), (b'RELOAD_PLUGIN', b'RELOAD_PLUGIN'), (b'RESTART_PLUGIN', b'RESTART_PLUGIN'), (b'DELEGATE_PLUGIN', b'DELEGATE_PLUGIN'), (b'UNDELEGATE_PLUGIN', b'UNDELEGATE_PLUGIN'), (b'UPGRADE_PLUGIN', b'UPGRADE_PLUGIN')]),
        ),
    ]
