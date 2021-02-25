# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0032_auto_20181211_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='cc_ip_types',
            field=models.CharField(max_length=45, null=True, verbose_name='\u6ce8\u518cCMDB\u7684IP\u7c7b\u578b', blank=True),
        ),
    ]
