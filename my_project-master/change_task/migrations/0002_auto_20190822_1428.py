# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('change_task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptinstance',
            name='custom_task',
            field=models.ForeignKey(related_name='custom_script_instances', blank=True, to='change_task.CustomTask', help_text='\u81ea\u5b9a\u4e49\u4efb\u52a1', null=True),
        ),
        migrations.AlterField(
            model_name='scriptinstance',
            name='scene_task',
            field=models.ForeignKey(related_name='scene_script_instances', blank=True, to='change_task.SceneTask', help_text='\u573a\u666f\u4efb\u52a1', null=True),
        ),
    ]
