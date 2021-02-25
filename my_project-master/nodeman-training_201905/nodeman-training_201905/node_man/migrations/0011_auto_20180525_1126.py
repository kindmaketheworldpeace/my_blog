# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0010_ip_sshkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloud',
            name='bk_cloud_id',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='cloud',
            name='bk_cloud_name',
            field=models.CharField(max_length=45),
        ),
    ]
