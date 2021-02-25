# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0031_auto_20181128_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='data_ip',
            field=models.CharField(max_length=45, null=True, verbose_name='\u6570\u636eIP', blank=True),
        ),
        migrations.AddField(
            model_name='host',
            name='login_ip',
            field=models.CharField(max_length=45, null=True, verbose_name='\u767b\u5f55IP', blank=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='inner_ip',
            field=models.CharField(max_length=45, verbose_name='\u901a\u4fe1IP'),
        ),
        migrations.AlterField(
            model_name='host',
            name='outer_ip',
            field=models.CharField(max_length=45, null=True, verbose_name='\u7ea7\u8054IP', blank=True),
        ),
        migrations.AlterField(
            model_name='tasklog',
            name='level',
            field=models.CharField(default=b'user', max_length=45, choices=[(b'user', b'user'), (b'warning', b'warning'), (b'error', b'error'), (b'info', b'info'), (b'debug', b'debug')]),
        ),
    ]
