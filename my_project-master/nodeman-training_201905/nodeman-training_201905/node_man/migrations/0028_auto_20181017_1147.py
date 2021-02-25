# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0027_proccontrol_os'),
    ]

    operations = [
        migrations.RenameField(
            model_name='packages',
            old_name='cpu_arc',
            new_name='cpu_arch',
        ),
        migrations.AlterField(
            model_name='gseplugindesc',
            name='config_format',
            field=models.CharField(default='json', max_length=32, verbose_name='\u914d\u7f6e\u6587\u4ef6\u683c\u5f0f\u7c7b\u578b', choices=[(b'json', b'json'), (b'yaml', b'yaml'), (b'', b'')]),
        ),
    ]
