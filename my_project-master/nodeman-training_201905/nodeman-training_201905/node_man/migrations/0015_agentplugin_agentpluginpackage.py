# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0014_auto_20180711_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentPlugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name='\u63d2\u4ef6\u540d')),
                ('desc', models.CharField(max_length=128, verbose_name='\u63d2\u4ef6\u63cf\u8ff0')),
                ('scenario', models.CharField(max_length=32, verbose_name='\u4f7f\u7528\u573a\u666f')),
                ('category', models.CharField(max_length=32, verbose_name='\u6240\u5c5e\u8303\u56f4')),
                ('config_file', models.CharField(max_length=128, verbose_name='\u914d\u7f6e\u6587\u4ef6\u540d\u79f0')),
                ('config_format', models.CharField(max_length=32, verbose_name='\u914d\u7f6e\u6587\u4ef6\u683c\u5f0f\u7c7b\u578b')),
                ('use_db', models.SmallIntegerField(verbose_name='\u662f\u5426\u4f7f\u7528\u6570\u636e\u5e93')),
                ('is_binary', models.SmallIntegerField(verbose_name='\u662f\u5426\u4e8c\u8fdb\u5236\u6587\u4ef6')),
            ],
        ),
        migrations.CreateModel(
            name='AgentPluginPackage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pkg_name', models.CharField(max_length=128, verbose_name='\u63d2\u4ef6\u5305\u540d')),
                ('version', models.CharField(max_length=128, verbose_name='\u63d2\u4ef6\u7248\u672c\u53f7')),
                ('module', models.CharField(max_length=32, verbose_name='\u6240\u5c5e\u670d\u52a1')),
                ('project', models.CharField(max_length=128, verbose_name='\u63d2\u4ef6\u540d')),
                ('pkg_size', models.IntegerField(verbose_name='\u5305\u5927\u5c0f')),
                ('pkg_path', models.CharField(max_length=128, verbose_name='\u5305\u8def\u5f84')),
                ('md5', models.CharField(max_length=32, verbose_name='md5\u503c')),
                ('pkg_mtime', models.CharField(max_length=48, verbose_name='\u5305\u66f4\u65b0\u65f6\u95f4')),
                ('pkg_ctime', models.CharField(max_length=48, verbose_name='\u5305\u521b\u5efa\u65f6\u95f4')),
                ('location', models.CharField(max_length=512, verbose_name='\u5305\u4e0b\u8f7d\u94fe\u63a5')),
            ],
        ),
    ]
