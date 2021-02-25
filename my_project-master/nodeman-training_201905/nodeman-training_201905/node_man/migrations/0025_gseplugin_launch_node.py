# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0024_auto_20181004_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='gseplugin',
            name='launch_node',
            field=models.CharField(default='all', max_length=32, verbose_name='\u5bbf\u4e3b\u8282\u70b9\u7c7b\u578b\u8981\u6c42', choices=[('agent', 'agent'), ('proxy', 'proxy'), ('all', 'all')]),
        ),
    ]
