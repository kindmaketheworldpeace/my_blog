# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0003_auto_20180409_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklog',
            name='flag',
            field=models.CharField(default=b'EMPTY', max_length=45, verbose_name='\u989d\u5916\u6807\u8bb0', choices=[(b'STEP', b'STEP'), (b'EMPTY', b'EMPTY')]),
        ),
    ]
