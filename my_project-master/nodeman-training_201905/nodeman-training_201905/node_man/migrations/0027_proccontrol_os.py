# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0026_auto_20181014_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='proccontrol',
            name='os',
            field=models.CharField(default=b'linux', max_length=32, verbose_name='\u7cfb\u7edf\u7c7b\u578b', choices=[(b'windows', b'windows'), (b'linux', b'linux'), (b'aix', b'aix')]),
        ),
    ]
