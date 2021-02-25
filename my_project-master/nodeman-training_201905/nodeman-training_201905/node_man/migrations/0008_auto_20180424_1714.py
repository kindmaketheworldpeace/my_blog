# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0007_auto_20180413_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloud',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5220\u9664'),
        ),
        migrations.AddField(
            model_name='cloud',
            name='is_visible',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u89c1'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_CONFIG', b'UPDATE_CONFIG'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO'), (b'UPGRADE_PROXY', b'UPGRADE_PROXY'), (b'UPGRADE_AGENT', b'UPGRADE_AGENT'), (b'UPGRADE_PAGENT', b'UPGRADE_PAGENT')]),
        ),
    ]
