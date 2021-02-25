# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0013_ip_sshkey_confirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='bk_cloud_id',
            field=models.CharField(max_length=45, verbose_name='\u4e91\u533a\u57dfID'),
        ),
    ]
