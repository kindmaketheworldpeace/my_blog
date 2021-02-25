# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0017_auto_20180827_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processinfo',
            name='scenario',
            field=models.CharField(max_length=256, verbose_name='\u4f7f\u7528\u573a\u666f'),
        ),
    ]
