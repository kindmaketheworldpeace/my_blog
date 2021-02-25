# -*- coding: utf-8 -*-

from blueking.component.shortcuts import get_client_by_user
from common.mymako import render_json
import json


def get_host_by_module(request):
    client = get_client_by_user("admin")
    bk_module_name = request.GET.get("bk_module_name")

    kw = {
        "ip": {
            "data": [],
            "exact": 1,
            "flag": "bk_host_innerip|bk_host_outerip"
        },
        "condition": [

            {
                "bk_obj_id": "host",
                "fields": [],
                "condition": [
                ]
            },
            {
                "bk_obj_id": "module",
                "fields": [],
                "condition": [
                    {
                        "field": "bk_module_name",
                        "operator": "$eq",
                        "value": bk_module_name,
                    }
                ]
            }

        ],
    }
    res = client.cc.search_host(kw)
    print res
    return render_json({"result": True, "data": res["data"]["info"]})


def get_host(request):
    client = get_client_by_user("admin")
    data = json.loads(request.body)
    limit = data.get("limit", 10)
    page = data.get("page", 1)
    if limit > 200:
        return render_json({"result": False, "message": u"最大限制为200！"})
    ip = data.get("ip", [])
    kw = {
        "ip": {
            "data": ip,
            "exact": 1,
            "flag": "bk_host_innerip|bk_host_outerip"
        },
        "condition": [
            {
                "bk_obj_id": "host",
                "fields": [],
                "condition": []
            },

            {
                "bk_obj_id": "biz",
                "fields": [],
                "condition": []
            },
        ],
        "page": {
            "start": (page - 1) * limit,
            "limit": limit,
            "sort": "bk_host_id"
        },

    }
    res = client.cc.search_host(kw)
    return render_json({"result": True, "data": res["data"]["info"]})


def get_bk_user(request):
    client = get_client_by_user("admin")
    kw = {
    }
    res = client.bk_login.get_all_users(kw)
    if res["result"]:
        return render_json({"result": True, "data": res["data"]})
