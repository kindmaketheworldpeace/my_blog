# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.CharField(max_length=64, null=True, verbose_name='\u521b\u5efa\u4eba', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('updated_by', models.CharField(max_length=64, null=True, verbose_name='\u4fee\u6539\u4eba', blank=True)),
                ('end_at', models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8f6f\u5220\u9664')),
                ('name', models.CharField(max_length=64, verbose_name='\u81ea\u5b9a\u4e49\u4efb\u52a1\u540d\u79f0')),
                ('serivce_privider', models.CharField(max_length=32, verbose_name='\u670d\u52a1\u5546')),
                ('account', models.CharField(max_length=32, verbose_name='\u670d\u52a1\u5668\u5e10\u6237')),
                ('biz_list', jsonfield.fields.JSONField(default=[], verbose_name='\u4e1a\u52a1')),
                ('ip_list', jsonfield.fields.JSONField(default=[], verbose_name='\u76ee\u6807\u673a\u5668')),
                ('script_type', models.IntegerField(verbose_name='\u811a\u672c\u6765\u6e90', choices=[(1, b'shell'), (2, b'bat'), (3, b'perl'), (4, b'python'), (5, b'powershell')])),
                ('script_param', models.CharField(max_length=128, verbose_name='\u811a\u672c\u53c2\u6570')),
                ('script_content', models.TextField(verbose_name='\u811a\u672c\u5185\u5bb9', blank=True)),
                ('script_timeout', models.IntegerField(default=1000, verbose_name='\u8d85\u65f6\u65f6\u95f4(s)')),
                ('status', models.IntegerField(verbose_name='\u4efb\u52a1\u72b6\u6001', choices=[(1, '\u672a\u6267\u884c'), (2, '\u6b63\u5728\u6267\u884c'), (3, '\u6267\u884c\u6210\u529f'), (4, '\u6267\u884c\u5931\u8d25'), (13, '\u5df2\u62d2\u7edd'), (14, '\u5f85\u590d\u6838'), (15, '\u5f85\u5ba1\u6279')])),
                ('rule_info', jsonfield.fields.JSONField(default={}, verbose_name='\u5e94\u7528\u89c4\u5219\u8be6\u60c5')),
            ],
            options={
                'verbose_name': '\u81ea\u5b9a\u4e49\u4efb\u52a1',
                'verbose_name_plural': '\u81ea\u5b9a\u4e49\u4efb\u52a1',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.CharField(max_length=64, null=True, verbose_name='\u521b\u5efa\u4eba', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('updated_by', models.CharField(max_length=64, null=True, verbose_name='\u4fee\u6539\u4eba', blank=True)),
                ('end_at', models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8f6f\u5220\u9664')),
                ('name', models.CharField(max_length=64, verbose_name='\u89c4\u5219\u540d\u79f0')),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0\u4fe1\u606f', blank=True)),
                ('is_enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528')),
                ('condition', jsonfield.fields.JSONField(default=[], verbose_name='\u89c4\u5219\u6761\u4ef6')),
                ('result', models.CharField(max_length=32, verbose_name='\u89c4\u5219\u7ed3\u679c', choices=[(b'REJECT', '\u62d2\u7edd'), (b'CHECK', '\u590d\u6838'), (b'PASS', '\u901a\u8fc7')])),
            ],
            options={
                'verbose_name': '\u89c4\u5219',
                'verbose_name_plural': '\u89c4\u5219',
            },
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.CharField(max_length=64, null=True, verbose_name='\u521b\u5efa\u4eba', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('updated_by', models.CharField(max_length=64, null=True, verbose_name='\u4fee\u6539\u4eba', blank=True)),
                ('end_at', models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8f6f\u5220\u9664')),
                ('name', models.CharField(max_length=64, verbose_name='\u573a\u666f\u540d\u79f0')),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0\u4fe1\u606f', blank=True)),
                ('display_role', models.CharField(max_length=1024, verbose_name='\u53ef\u89c1\u8303\u56f4', blank=True)),
                ('display_type', models.CharField(default=b'OPEN', max_length=32, verbose_name='\u53ef\u89c1\u8303\u56f4\u7c7b\u578b', choices=[(b'CMDB', 'CMDB\u4e1a\u52a1\u516c\u7528\u89d2\u8272'), (b'GENERAL', '\u901a\u7528\u89d2\u8272\u8868'), (b'OPEN', '\u4e0d\u9650'), (b'PERSON', '\u4e2a\u4eba'), (b'EMPTY', '\u65e0')])),
                ('account', models.CharField(max_length=32, verbose_name='\u670d\u52a1\u5668\u5e10\u6237')),
                ('os_type', models.CharField(max_length=32, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7c7b\u578b', choices=[(b'LINUX', 'linux'), (b'WINDOWS', 'windows')])),
                ('script_type', models.IntegerField(verbose_name='\u811a\u672c\u6765\u6e90', choices=[(1, b'shell'), (2, b'bat'), (3, b'perl'), (4, b'python'), (5, b'powershell')])),
                ('input_display_list', jsonfield.fields.JSONField(default=[], verbose_name='\u811a\u672c\u53c2\u6570\u663e\u793a\u540d')),
                ('output_display_map', jsonfield.fields.JSONField(default={}, verbose_name='\u811a\u672c\u7ed3\u679c\u663e\u793a\u540d\u6620\u5c04')),
                ('script_content', models.TextField(verbose_name='\u811a\u672c\u5185\u5bb9', blank=True)),
                ('script_timeout', models.IntegerField(default=1000, verbose_name='\u8d85\u65f6\u65f6\u95f4(s)')),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': '\u573a\u666f',
                'verbose_name_plural': '\u573a\u666f',
            },
        ),
        migrations.CreateModel(
            name='SceneTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.CharField(max_length=64, null=True, verbose_name='\u521b\u5efa\u4eba', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('updated_by', models.CharField(max_length=64, null=True, verbose_name='\u4fee\u6539\u4eba', blank=True)),
                ('end_at', models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8f6f\u5220\u9664')),
                ('name', models.CharField(max_length=64, verbose_name='\u573a\u666f\u4efb\u52a1\u540d\u79f0')),
                ('serivce_privider', models.CharField(max_length=32, verbose_name='\u670d\u52a1\u5546')),
                ('account', models.CharField(max_length=32, verbose_name='\u670d\u52a1\u5668\u5e10\u6237')),
                ('biz_list', jsonfield.fields.JSONField(default=[], verbose_name='\u4e1a\u52a1')),
                ('ip_list', jsonfield.fields.JSONField(default=[], verbose_name='\u76ee\u6807\u673a\u5668')),
                ('script_type', models.IntegerField(verbose_name='\u811a\u672c\u6765\u6e90', choices=[(1, b'shell'), (2, b'bat'), (3, b'perl'), (4, b'python'), (5, b'powershell')])),
                ('input_display_list', jsonfield.fields.JSONField(default=[], verbose_name='\u811a\u672c\u53c2\u6570\u663e\u793a\u540d')),
                ('script_param', models.CharField(max_length=128, verbose_name='\u811a\u672c\u53c2\u6570')),
                ('output_display_map', jsonfield.fields.JSONField(default={}, verbose_name='\u811a\u672c\u7ed3\u679c\u663e\u793a\u540d\u6620\u5c04')),
                ('script_content', models.TextField(verbose_name='\u811a\u672c\u5185\u5bb9', blank=True)),
                ('script_timeout', models.IntegerField(default=1000, verbose_name='\u8d85\u65f6\u65f6\u95f4(s)')),
                ('status', models.IntegerField(verbose_name='\u4efb\u52a1\u72b6\u6001', choices=[(1, '\u672a\u6267\u884c'), (2, '\u6b63\u5728\u6267\u884c'), (3, '\u6267\u884c\u6210\u529f'), (4, '\u6267\u884c\u5931\u8d25'), (13, '\u5df2\u62d2\u7edd'), (14, '\u5f85\u590d\u6838'), (15, '\u5f85\u5ba1\u6279')])),
                ('rule_info', jsonfield.fields.JSONField(default={}, verbose_name='\u5e94\u7528\u89c4\u5219\u8be6\u60c5')),
                ('scene', models.ForeignKey(related_name='tasks', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='change_task.Scene', help_text='\u573a\u666f', null=True)),
            ],
            options={
                'verbose_name': '\u573a\u666f\u4efb\u52a1',
                'verbose_name_plural': '\u573a\u666f\u4efb\u52a1',
            },
        ),
        migrations.CreateModel(
            name='ScriptInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.CharField(max_length=64, null=True, verbose_name='\u521b\u5efa\u4eba', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('updated_by', models.CharField(max_length=64, null=True, verbose_name='\u4fee\u6539\u4eba', blank=True)),
                ('end_at', models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8f6f\u5220\u9664')),
                ('bk_biz_id', models.IntegerField(verbose_name='\u4e1a\u52a1ID')),
                ('job_instance_name', models.CharField(max_length=64, verbose_name='\u811a\u672c\u5b9e\u4f8b\u540d\u79f0')),
                ('job_instance_id', models.IntegerField(verbose_name='\u811a\u672c\u5b9e\u4f8bID')),
                ('status', models.IntegerField(verbose_name='\u811a\u672c\u5b9e\u4f8b\u72b6\u6001', choices=[(1, '\u672a\u6267\u884c'), (2, '\u6b63\u5728\u6267\u884c'), (3, '\u6267\u884c\u6210\u529f'), (4, '\u6267\u884c\u5931\u8d25'), (5, '\u8df3\u8fc7'), (6, '\u5ffd\u7565\u9519\u8bef'), (7, '\u7b49\u5f85\u7528\u6237'), (8, '\u624b\u52a8\u7ed3\u675f'), (9, '\u72b6\u6001\u5f02\u5e38'), (10, '\u6b65\u9aa4\u5f3a\u5236\u7ec8\u6b62\u4e2d'), (11, '\u6b65\u9aa4\u5f3a\u5236\u7ec8\u6b62\u6210\u529f'), (12, '\u6b65\u9aa4\u5f3a\u5236\u7ec8\u6b62\u6210\u529f')])),
                ('is_finished', models.BooleanField(default=False, verbose_name='\x08\u811a\u672c\u5b9e\u4f8b\u662f\u5426\u7ed3\u675f')),
                ('job_instance_type', models.CharField(max_length=32, verbose_name='\u811a\u672c\u5b9e\u4f8b\u7c7b\u578b', choices=[(b'CUSTOM', '\u81ea\u5b9a\u4e49'), (b'SCENE', '\u573a\u666f')])),
                ('plain_results', jsonfield.fields.JSONField(default=[], verbose_name='\u539f\u59cb\u7ed3\u679c\u65e5\u5fd7')),
                ('format_results', jsonfield.fields.JSONField(default=[], verbose_name='\u683c\u5f0f\u5316\u7ed3\u679c\u65e5\u5fd7')),
                ('custom_task', models.ForeignKey(related_name='custom_script_instances', to='change_task.CustomTask', help_text='\u81ea\u5b9a\u4e49\u4efb\u52a1')),
                ('scene_task', models.ForeignKey(related_name='scene_script_instances', to='change_task.SceneTask', help_text='\u573a\u666f\u4efb\u52a1')),
            ],
            options={
                'verbose_name': '\u811a\u672c\u5b9e\u4f8b',
                'verbose_name_plural': '\u811a\u672c\u5b9e\u4f8b',
            },
        ),
        migrations.CreateModel(
            name='ServicePrivider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creator', models.CharField(max_length=64, null=True, verbose_name='\u521b\u5efa\u4eba', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('updated_by', models.CharField(max_length=64, null=True, verbose_name='\u4fee\u6539\u4eba', blank=True)),
                ('end_at', models.DateTimeField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('is_deleted', models.BooleanField(default=False, db_index=True, verbose_name='\u662f\u5426\u8f6f\u5220\u9664')),
                ('name', models.CharField(max_length=64, verbose_name='\u670d\u52a1\u5546\u540d\u79f0')),
                ('description', models.TextField(verbose_name='\u63cf\u8ff0\u4fe1\u606f', blank=True)),
                ('checkers', models.CharField(max_length=1024, verbose_name='\u590d\u6838\u8005', blank=True)),
                ('checkers_type', models.CharField(default=b'PERSON', max_length=32, verbose_name='\u590d\u6838\u8005\u7c7b\u578b', choices=[(b'CMDB', 'CMDB\u4e1a\u52a1\u516c\u7528\u89d2\u8272'), (b'GENERAL', '\u901a\u7528\u89d2\u8272\u8868'), (b'OPEN', '\u4e0d\u9650'), (b'PERSON', '\u4e2a\u4eba'), (b'EMPTY', '\u65e0')])),
                ('approvers', models.CharField(max_length=1024, verbose_name='\u5ba1\u6279\u8005', blank=True)),
                ('approvers_type', models.CharField(default=b'PERSON', max_length=32, verbose_name='\u5ba1\u6279\u8005\u7c7b\u578b', choices=[(b'CMDB', 'CMDB\u4e1a\u52a1\u516c\u7528\u89d2\u8272'), (b'GENERAL', '\u901a\u7528\u89d2\u8272\u8868'), (b'OPEN', '\u4e0d\u9650'), (b'PERSON', '\u4e2a\u4eba'), (b'EMPTY', '\u65e0')])),
                ('rule_priority_list', jsonfield.fields.JSONField(default=[], verbose_name='\u89c4\u5219\u4f18\u5148\u7ea7\u6392\u5e8f')),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5546',
                'verbose_name_plural': '\u670d\u52a1\u5546',
            },
        ),
        migrations.AddField(
            model_name='rule',
            name='service_privider',
            field=models.ForeignKey(related_name='rules', to='change_task.ServicePrivider', help_text='\u670d\u52a1\u5546'),
        ),
    ]
