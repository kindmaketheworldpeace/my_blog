# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0019_merge'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProcessInfo',
            new_name='GsePlugin',
        ),
        migrations.AlterModelOptions(
            name='processcontrolinfo',
            options={'verbose_name': '\u6a21\u5757/\u5de5\u7a0b\u63a7\u5236\u4fe1\u606f\u8868', 'verbose_name_plural': '\u6a21\u5757/\u5de5\u7a0b\u63a7\u5236\u4fe1\u606f\u8868'},
        ),
        migrations.AlterModelOptions(
            name='processpackage',
            options={'verbose_name': '\u6a21\u5757/\u5de5\u7a0b\u5b89\u88c5\u5305\u4fe1\u606f\u8868', 'verbose_name_plural': '\u6a21\u5757/\u5de5\u7a0b\u5b89\u88c5\u5305\u4fe1\u606f\u8868'},
        ),
        migrations.AlterField(
            model_name='processcontrolinfo',
            name='project',
            field=models.CharField(max_length=32, verbose_name='\u5de5\u7a0b\u540d'),
        ),
        migrations.AlterField(
            model_name='processpackage',
            name='location',
            field=models.CharField(max_length=512, verbose_name='\u5b89\u88c5\u5305\u94fe\u63a5'),
        ),
        migrations.AlterField(
            model_name='processpackage',
            name='pkg_name',
            field=models.CharField(max_length=128, verbose_name='\u538b\u7f29\u5305\u540d'),
        ),
        migrations.AlterField(
            model_name='processpackage',
            name='project',
            field=models.CharField(max_length=32, verbose_name='\u5de5\u7a0b\u540d'),
        ),
        migrations.AlterField(
            model_name='processpackage',
            name='version',
            field=models.CharField(max_length=128, verbose_name='\u7248\u672c\u53f7'),
        ),
    ]
