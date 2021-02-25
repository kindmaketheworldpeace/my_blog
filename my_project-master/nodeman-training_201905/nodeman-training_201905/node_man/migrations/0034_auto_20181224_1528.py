# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node_man', '0033_host_cc_ip_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='auth_type',
            field=models.CharField(default=b'PASSWORD', max_length=45, choices=[(b'PASSWORD', b'PASSWORD'), (b'KEY', b'KEY'), (b'CERT_KEY', b'CERT_KEY')]),
        ),
        migrations.AlterField(
            model_name='host',
            name='bk_supplier_account',
            field=models.CharField(default='0', max_length=45, null=True, verbose_name='\u670d\u52a1\u5546', blank=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='bk_supplier_id',
            field=models.CharField(default='0', max_length=45, null=True, verbose_name='\u670d\u52a1\u5546ID', blank=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='cc_ip_types',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u6ce8\u518cCMDB\u7684IP\u7c7b\u578b', blank=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='data_ip',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u6570\u636eIP', blank=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='login_ip',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u767b\u5f55IP', blank=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='outer_ip',
            field=models.CharField(default='', max_length=45, null=True, verbose_name='\u7ea7\u8054IP', blank=True),
        ),
    ]
