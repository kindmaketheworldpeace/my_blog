# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0002_auto_20180403_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u88ab\u53d6\u6d88\u4efb\u52a1'),
        ),
        migrations.AlterField(
            model_name='host',
            name='agent_status',
            field=models.IntegerField(default=0, verbose_name='agent\u8fd0\u884c\u72b6\u6001', choices=[(0, b'UNKNOWN'), (1, b'RUNNING'), (2, b'TERMINATED')]),
        ),
    ]
