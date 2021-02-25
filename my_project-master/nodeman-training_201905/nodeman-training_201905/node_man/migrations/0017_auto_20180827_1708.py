# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0016_auto_20180822_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u63d2\u4ef6\u540d')),
                ('description', models.CharField(max_length=128, verbose_name='\u63d2\u4ef6\u63cf\u8ff0')),
                ('scenario', models.CharField(max_length=32, verbose_name='\u4f7f\u7528\u573a\u666f')),
                ('category', models.CharField(max_length=32, verbose_name='\u6240\u5c5e\u8303\u56f4', choices=[(b'official', b'official'), (b'external', b'external'), (b'scripts', b'scripts')])),
                ('config_file', models.CharField(max_length=128, verbose_name='\u914d\u7f6e\u6587\u4ef6\u540d\u79f0')),
                ('config_file_format', models.CharField(default='json', max_length=32, verbose_name='\u914d\u7f6e\u6587\u4ef6\u683c\u5f0f\u7c7b\u578b', choices=[(b'json', b'json'), (b'yaml', b'yaml')])),
                ('use_db', models.BooleanField(default=0, verbose_name='\u662f\u5426\u4f7f\u7528\u6570\u636e\u5e93')),
                ('is_binary', models.BooleanField(default=1, verbose_name='\u662f\u5426\u4e8c\u8fdb\u5236\u6587\u4ef6')),
            ],
            options={
                'verbose_name': '\u63d2\u4ef6\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u63d2\u4ef6\u4fe1\u606f\u8868',
            },
        ),
        migrations.RenameModel(
            old_name='ProcessControl',
            new_name='ProcessControlInfo',
        ),
        migrations.RenameModel(
            old_name='AgentPluginPackage',
            new_name='ProcessPackage',
        ),
        migrations.DeleteModel(
            name='AgentPlugin',
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_CONFIG', b'UPDATE_CONFIG'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO'), (b'UPGRADE_PROXY', b'UPGRADE_PROXY'), (b'UPGRADE_AGENT', b'UPGRADE_AGENT'), (b'UPGRADE_PAGENT', b'UPGRADE_PAGENT'), (b'START_PLUGIN', b'START_PLUGIN'), (b'STOP_PLUGIN', b'STOP_PLUGIN'), (b'RELOAD_PLUGIN', b'RELOAD_PLUGIN'), (b'RESTART_PLUGIN', b'RESTART_PLUGIN'), (b'DELEGATE_PLUGIN', b'DELEGATE_PLUGIN'), (b'UNDELEGATE_PLUGIN', b'UNDELEGATE_PLUGIN'), (b'UPGRADE_PLUGIN', b'UPGRADE_PLUGIN')]),
        ),
    ]
