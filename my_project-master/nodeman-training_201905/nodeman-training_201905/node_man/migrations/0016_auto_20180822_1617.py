# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0015_agentplugin_agentpluginpackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessControl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('module', models.CharField(max_length=32, verbose_name='\u6a21\u5757\u540d')),
                ('project', models.CharField(max_length=32, verbose_name='\u8fdb\u7a0b\u540d')),
                ('install_path', models.CharField(max_length=128, verbose_name='\u5b89\u88c5\u8def\u5f84')),
                ('log_path', models.CharField(max_length=128, verbose_name='\u65e5\u5fd7\u8def\u5f84')),
                ('data_path', models.CharField(max_length=128, verbose_name='\u6570\u636e\u6587\u4ef6\u8def\u5f84')),
                ('pid_path', models.CharField(max_length=128, verbose_name='pid\u6587\u4ef6\u8def\u5f84')),
                ('start_cmd', models.CharField(max_length=128, verbose_name='\u542f\u52a8\u547d\u4ee4')),
                ('stop_cmd', models.CharField(max_length=128, verbose_name='\u505c\u6b62\u547d\u4ee4')),
                ('restart_cmd', models.CharField(max_length=128, verbose_name='\u91cd\u542f\u547d\u4ee4')),
                ('reload_cmd', models.CharField(max_length=128, verbose_name='\u91cd\u8f7d\u547d\u4ee4')),
            ],
            options={
                'verbose_name': '\u8fdb\u7a0b\u5b89\u88c5\u4fe1\u606f\u8868',
                'verbose_name_plural': '\u8fdb\u7a0b\u5b89\u88c5\u4fe1\u606f\u8868',
            },
        ),
        migrations.AlterModelOptions(
            name='agentplugin',
            options={'verbose_name': '\u63d2\u4ef6\u4fe1\u606f\u8868', 'verbose_name_plural': '\u63d2\u4ef6\u4fe1\u606f\u8868'},
        ),
        migrations.AlterModelOptions(
            name='agentpluginpackage',
            options={'verbose_name': '\u63d2\u4ef6\u5305\u4fe1\u606f\u8868', 'verbose_name_plural': '\u63d2\u4ef6\u5305\u4fe1\u606f\u8868'},
        ),
        migrations.RenameField(
            model_name='agentplugin',
            old_name='desc',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='agentplugin',
            name='config_format',
        ),
        migrations.AddField(
            model_name='agentplugin',
            name='config_file_format',
            field=models.CharField(default='json', max_length=32, verbose_name='\u914d\u7f6e\u6587\u4ef6\u683c\u5f0f\u7c7b\u578b', choices=[(b'json', b'json'), (b'yaml', b'yaml')]),
        ),
        migrations.AddField(
            model_name='job',
            name='global_params',
            field=models.TextField(null=True, verbose_name='\u5168\u5c40\u8fd0\u884c\u53c2\u6570', blank=True),
        ),
        migrations.AlterField(
            model_name='agentplugin',
            name='category',
            field=models.CharField(max_length=32, verbose_name='\u6240\u5c5e\u8303\u56f4', choices=[(b'official', b'official'), (b'external', b'external'), (b'scripts', b'scripts')]),
        ),
        migrations.AlterField(
            model_name='agentplugin',
            name='is_binary',
            field=models.SmallIntegerField(default=1, verbose_name='\u662f\u5426\u4e8c\u8fdb\u5236\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='agentplugin',
            name='use_db',
            field=models.SmallIntegerField(default=0, verbose_name='\u662f\u5426\u4f7f\u7528\u6570\u636e\u5e93'),
        ),
        migrations.AlterField(
            model_name='agentpluginpackage',
            name='project',
            field=models.CharField(max_length=32, verbose_name='\u63d2\u4ef6\u540d'),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_type',
            field=models.CharField(default=b'INSTALL_PROXY', max_length=45, verbose_name='\u4f5c\u4e1a\u7c7b\u578b', choices=[(b'INSTALL_PROXY', b'INSTALL_PROXY'), (b'INSTALL_AGENT', b'INSTALL_AGENT'), (b'INSTALL_PAGENT', b'INSTALL_PAGENT'), (b'REINSTALL_PROXY', b'REINSTALL_PROXY'), (b'REINSTALL_AGENT', b'REINSTALL_AGENT'), (b'REINSTALL_PAGENT', b'REINSTALL_PAGENT'), (b'UNINSTALL_AGENT', b'UNINSTALL_AGENT'), (b'REMOVE_AGENT', b'REMOVE_AGENT'), (b'UPDATE_PLUGIN', b'UPDATE_PLUGIN'), (b'UPDATE_CONFIG', b'UPDATE_CONFIG'), (b'UPDATE_AUTHINFO', b'UPDATE_AUTHINFO'), (b'UPGRADE_PROXY', b'UPGRADE_PROXY'), (b'UPGRADE_AGENT', b'UPGRADE_AGENT'), (b'UPGRADE_PAGENT', b'UPGRADE_PAGENT'), (b'START_PLUGIN', b'START_PLUGIN'), (b'STOP_PLUGIN', b'STOP_PLUGIN'), (b'RELOAD_PLUGIN', b'RELOAD_PLUGIN'), (b'RESTART_PLUGIN', b'RESTART_PLUGIN'), (b'DELEGATE_PLUGIN', b'DELEGATE_PLUGIN'), (b'UNDELEGATE_PLUGIN', b'UNDELEGATE_PLUGIN')]),
        ),
    ]
