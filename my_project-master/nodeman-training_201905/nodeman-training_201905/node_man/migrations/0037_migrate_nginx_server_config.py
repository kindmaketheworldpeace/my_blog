# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations, models


def update_nginx_server(apps, schema):
    KV = apps.get_model("node_man", "KV")
    try:
        nginx_server = KV.objects.get(key="nginx")
        config = nginx_server.v_json
        if 'inner_ip' in config:
            new_config = {
                'inner_url': "http://{}/download/".format(config.get("inner_ip", "")),
                'outer_url': "http://{}/download/".format(config.get("outer_ip", ""))
            }
            nginx_server.v_json = new_config
            nginx_server.save()
    except Exception as err:
        print err


class Migration(migrations.Migration):
    dependencies = [("node_man", "0036_auto_20190314_1640")]
    operations = [migrations.RunPython(update_nginx_server)]
