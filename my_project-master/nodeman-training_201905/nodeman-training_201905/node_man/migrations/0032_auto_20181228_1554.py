# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0031_auto_20181128_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='level',
            field=models.CharField(default=b'user', max_length=45, choices=[(b'user', b'user'), (b'warning', b'warning'), (b'error', b'error'), (b'info', b'info'), (b'debug', b'debug')]),
        ),
    ]
