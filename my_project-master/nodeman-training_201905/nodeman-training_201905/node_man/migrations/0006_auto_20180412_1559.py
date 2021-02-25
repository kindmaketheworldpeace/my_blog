# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0005_auto_20180411_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='task_id',
            field=models.CharField(max_length=45, null=True, verbose_name='\u5173\u8054\u7684celery_id', blank=True),
        ),
    ]
