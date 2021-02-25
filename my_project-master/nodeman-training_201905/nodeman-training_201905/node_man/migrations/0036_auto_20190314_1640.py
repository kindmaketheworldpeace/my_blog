# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0035_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gseplugindesc',
            name='config_file',
            field=models.CharField(max_length=128, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6\u540d\u79f0', blank=True),
        ),
        migrations.AlterField(
            model_name='gseplugindesc',
            name='config_format',
            field=models.CharField(default='json', choices=[(b'json', b'json'), (b'yaml', b'yaml'), (b'', b''), (None, None)], max_length=32, blank=True, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6\u683c\u5f0f\u7c7b\u578b'),
        ),
    ]
