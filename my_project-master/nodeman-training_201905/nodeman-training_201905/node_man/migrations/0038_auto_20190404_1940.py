# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0037_migrate_nginx_server_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='gseplugindesc',
            name='description_en',
            field=models.CharField(max_length=128, null=True, verbose_name='\u82f1\u6587\u63d2\u4ef6\u63cf\u8ff0', blank=True),
        ),
        migrations.AddField(
            model_name='gseplugindesc',
            name='scenario_en',
            field=models.CharField(max_length=256, null=True, verbose_name='\u82f1\u6587\u4f7f\u7528\u573a\u666f', blank=True),
        ),
    ]
