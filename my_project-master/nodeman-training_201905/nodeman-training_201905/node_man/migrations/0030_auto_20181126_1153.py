# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0029_auto_20181114_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='bk_supplier_account',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u670d\u52a1\u5546', blank=True),
        ),
        migrations.AddField(
            model_name='host',
            name='bk_supplier_id',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u670d\u52a1\u5546ID', blank=True),
        ),
    ]
