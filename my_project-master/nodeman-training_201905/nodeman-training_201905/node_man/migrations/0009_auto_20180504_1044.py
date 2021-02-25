# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0008_auto_20180424_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='update_time',
            field=models.DateTimeField(null=True, verbose_name='agent\u66f4\u65b0\u65f6\u95f4'),
        ),
    ]
