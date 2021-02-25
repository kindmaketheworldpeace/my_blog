# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from node_man.models import Cloud


def confirm_cloud_biz(apps, schema_editor):
    Host = apps.get_model("node_man", "Host")
    try:
        Cloud.cache_all_cloud()
        print u'sync cloud info success'
    except Exception as e:
        print "sync cloud info failed"

    hosts = Host.objects.filter(is_deleted=False)
    try:
        for host in hosts:
            cloud_id = host.bk_cloud_id
            if cloud_id == 0:
                continue
            biz_id = host.bk_biz_id
            cloud = Cloud.objects.filter(bk_cloud_id=cloud_id, is_deleted=False)
            if cloud.exists() and not cloud.filter(bk_biz_id=biz_id).exists():
                Cloud.objects.create(bk_cloud_id=cloud_id,
                                     bk_biz_id=biz_id,
                                     creator="system",
                                     bk_supplier_id=cloud[0].bk_supplier_id,
                                     bk_cloud_name=cloud[0].bk_cloud_name
                                     )
    except Exception as e:
        print str(e)


class Migration(migrations.Migration):
    dependencies = [
        ('node_man', '0012_auto_20180702_1637'),
        ('requests_tracker', '0002_record_request_host')
    ]

    operations = [
        (migrations.RunPython(confirm_cloud_biz)),
    ]
