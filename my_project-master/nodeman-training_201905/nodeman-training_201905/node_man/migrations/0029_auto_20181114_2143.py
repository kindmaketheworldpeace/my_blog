# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0028_auto_20181017_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='bk_supplier_account',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u670d\u52a1\u5546', blank=True),
        ),
        migrations.AddField(
            model_name='job',
            name='bk_supplier_id',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u670d\u52a1\u5546ID', blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPGRADE_PROXY', b'UPGRADE_PROXY'), (b'UPGRADE_AGENT', b'UPGRADE_AGENT'), (b'UPGRADE_PAGENT', b'UPGRADE_PAGENT'), (b'IMPORT_PROXY', b'IMPORT_PROXY'), (b'IMPORT_AGENT', b'IMPORT_AGENT'), (b'IMPORT_PAGENT', b'IMPORT_PAGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'START_PLUGIN', b'START_PLUGIN'), (b'STOP_PLUGIN', b'STOP_PLUGIN'), (b'RELOAD_PLUGIN', b'RELOAD_PLUGIN'), (b'RESTART_PLUGIN', b'RESTART_PLUGIN'), (b'DELEGATE_PLUGIN', b'DELEGATE_PLUGIN'), (b'UNDELEGATE_PLUGIN', b'UNDELEGATE_PLUGIN'), (b'UPGRADE_PLUGIN', b'UPGRADE_PLUGIN'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO')]),
        ),
    ]
