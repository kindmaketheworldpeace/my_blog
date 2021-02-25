# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('change_task', '0002_auto_20190822_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='scene',
            name='is_use',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u542f\u7528'),
        ),
    ]
