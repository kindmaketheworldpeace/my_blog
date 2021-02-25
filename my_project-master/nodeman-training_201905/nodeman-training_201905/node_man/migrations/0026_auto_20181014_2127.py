# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0025_gseplugin_launch_node'),
    ]

    operations = [
        migrations.RenameModel(
            'GsePlugin', 'GsePluginDesc'
        ),
        migrations.RenameModel(
            'ProcessControlInfo', 'ProcControl'
        ),
        migrations.RenameModel(
            'ProcessPackage', 'Packages'
        ),
    ]
