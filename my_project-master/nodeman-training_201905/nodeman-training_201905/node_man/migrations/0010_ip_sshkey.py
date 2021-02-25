# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from node_man.models import Cloud


def init_agent_data(apps, schema_editor):
    Agent_IP = apps.get_model("node_man", "IP")
    Host = apps.get_model("node_man", "Host")
    try:
        Cloud.cache_all_cloud()
        print u'sync cloud info success'
    except Exception as e:
        print "sync cloud info failed"

    try:
        ips = Agent_IP.objects.using("agent_setup").all()
    except Exception as e:
        print str(e)
        ips = []
    try:
        for ip in ips:
            plat_id = ip.plat_id.split("_")[0] if ip.plat_id else 0
            host, created = Host.objects.using("default").get_or_create(inner_ip=ip.inner_ip,
                                                                        bk_cloud_id=plat_id,
                                                                        bk_biz_id=ip.biz_id,
                                                                        is_deleted=False)
            if created:
                try:
                    node_type = 'agent' if ip.type == 1 else 'proxy'
                    (plat_id, supplier_id) = tuple(ip.plat_id.split("_"))
                    host.os_type = ip.os_type.upper()
                    host.auth_type = 'KEY' if ip.auth_type else 'PASSWORD'
                    host.has_cygwin = ip.has_cygwin
                    host.port = ip.port
                    host.account = ip.account
                    host.outer_ip = ip.outer_ip
                    host.node_type = 'PAGENT' if plat_id != str(0) and node_type == 'agent' else node_type.upper()
                    host.is_deleted = True if (ip.modify_type == 2 and ip.modify_status == 3) else False
                    host.save()
                except:
                    print "data error, ignore error and continue to migrate the next"
                    continue
                # 更新云区域信息
                try:
                    Cloud.objects.get(bk_cloud_id=host.bk_cloud_id, bk_biz_id=host.bk_biz_id)
                except Cloud.DoesNotExist:
                    Cloud.objects.filter(bk_cloud_id=host.bk_cloud_id, bk_biz_id='-1',
                                         bk_supplier_id=supplier_id or 0).update(bk_biz_id=host.bk_biz_id)
    except Exception as e:
        print str(e)


class Migration(migrations.Migration):
    dependencies = [
        ('node_man', '0009_auto_20180504_1044'),
        ('requests_tracker', '0002_record_request_host')
    ]

    operations = [
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('biz_id', models.CharField(max_length=128,
                                            verbose_name='\u4e1a\u52a1id\uff0c\u7528\u4e8e\u8fc7\u6ee4\u4e2d\u8f6c\u673a')),
                ('plat_id', models.CharField(max_length=128, verbose_name='\u6240\u5c5e\u4e91\u5e73\u53f0id')),
                ('inner_ip', models.GenericIPAddressField(verbose_name='\u4e3b\u673a\u5185\u7f51IP')),
                ('outer_ip',
                 models.GenericIPAddressField(default='', null=True, verbose_name='\u4e3b\u673a\u5916\u7f51IP',
                                              blank=True)),
                ('auth_type', models.SmallIntegerField(default=0, verbose_name='\u8ba4\u8bc1\u7c7b\u578b')),
                ('err_code', models.SmallIntegerField(default=0, verbose_name='\u5b89\u88c5\u9519\u8bef\u7801')),
                ('desc', models.CharField(default='', max_length=255, verbose_name='\u9519\u8bef\u63cf\u8ff0')),
                ('status', models.SmallIntegerField(default=0, verbose_name='\u5b89\u88c5\u7ed3\u679c')),
                ('type', models.SmallIntegerField(default=0, verbose_name='\u673a\u5668\u7c7b\u578b\uff0cproxy/agent')),
                ('account', models.CharField(max_length=128, verbose_name='SSH\u767b\u5f55\u7528\u6237')),
                ('password', models.CharField(max_length=128, verbose_name='SSH\u767b\u5f55\u5bc6\u7801', blank=True)),
                ('port', models.IntegerField(default=22, verbose_name='SSH\u767b\u5f55\u7aef\u53e3')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('start_time',
                 models.DateTimeField(auto_now_add=True, verbose_name='\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4')),
                ('end_time', models.DateTimeField(null=True, verbose_name='\u4efb\u52a1\u7ed3\u675f\u65f6\u95f4')),
                ('is_public', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5171\u4eab')),
                ('is_poped', models.BooleanField(default=False,
                                                 verbose_name='\u662f\u5426\u5f39\u51fa\u8fc7\u9519\u8bef\u4fe1\u606f')),
                ('modify_status', models.SmallIntegerField(default=0, verbose_name='\u53d8\u66f4\u72b6\u6001\u7801')),
                ('modify_type', models.SmallIntegerField(default=0,
                                                         verbose_name='\u53d8\u66f4\u7c7b\u578b\uff08\u5378\u8f7d/\u5237\u65b0\u914d\u7f6e\uff09')),
                ('expiry_time', models.DateTimeField(null=True,
                                                     verbose_name='\u5bc6\u7801\u6216\u5bc6\u94a5\u5931\u6548\u65f6\u95f4')),
                ('version', models.CharField(default='', max_length=128,
                                             verbose_name='\u5b9e\u65f6agent\u7248\u672c\u53f7\uff08\u6682\u672a\u542f\u7528\uff09',
                                             blank=True)),
                ('os_type',
                 models.CharField(default='Linux', max_length=32, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7c7b\u578b',
                                  choices=[('Windows', 'Windows'), ('Linux', 'Linux'), ('Aix', 'Aix')])),
                ('has_cygwin', models.SmallIntegerField(default=0, verbose_name='\u662f\u5426\u6709cygwin',
                                                        choices=[(0, '\u6ca1\u6709'), (1, '\u6709'),
                                                                 (2, '\u4e0d\u9700\u8981')])),
                ('exist', models.SmallIntegerField(default=0,
                                                   verbose_name='\u5b9e\u65f6agent\u72b6\u6001\uff08\u6682\u672a\u542f\u7528\uff09')),
            ],
            options={
                'ordering': ['is_public', '-create_time'],
                'verbose_name': 'IP\u4fe1\u606f',
                'db_table': 'miya_ip',
                'managed': False,
                'verbose_name_plural': 'IP\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='SshKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key_name', models.CharField(max_length=128, verbose_name='\u5bc6\u94a5\u6587\u4ef6\u540d')),
                ('key_path', models.CharField(max_length=255, verbose_name='\u5bc6\u94a5\u6587\u4ef6\u8def\u5f84')),
                ('key_content', models.TextField(max_length=255, verbose_name='\u5bc6\u94a5\u6587\u4ef6\u5185\u5bb9')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u4e0a\u4f20\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '\u5bc6\u94a5\u6587\u4ef6\u4fe1\u606f',
                'db_table': 'miya_sshkey',
                'managed': False,
                'verbose_name_plural': '\u5bc6\u94a5\u6587\u4ef6\u4fe1\u606f',
            },
        ),
        (migrations.RunPython(init_agent_data)),
    ]
