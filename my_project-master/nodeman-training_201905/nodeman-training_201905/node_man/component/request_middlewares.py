# -*- coding: utf-8 -*-
from django.dispatch import Signal
from node_man.utils.local import local
from blueking.component.shortcuts import get_client_by_request


class AccessorSignal(Signal):
    allowed_receiver = 'node_man.component.request_middlewares.RequestProvider'

    def __init__(self, providing_args=None):
        Signal.__init__(self, providing_args)

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
        receiver_name = '.'.join(
            [receiver.__class__.__module__, receiver.__class__.__name__]
        )
        if receiver_name != self.allowed_receiver:
            raise Exception(
                u"%s is not allowed to connect" % receiver_name)
        if not self.receivers:
            Signal.connect(self, receiver, sender, weak, dispatch_uid)


request_accessor = AccessorSignal()


class RequestProvider(object):
    """
    @summary: request事件接收者
    """

    def __init__(self):
        request_accessor.connect(self)

    def process_request(self, request):
        # try:
        #     client = get_client_by_request(request)
        #     client.set_bk_api_ver("v2")
        #     request.user.bk_supplier_account, request.user.bk_supplier_id = [
        #         client.bk_login.get_user()["data"].get(attr) for attr in
        #         ("bk_supplier_account", "bk_supplier_id")]
        #     print "@@@"*33
        # except Exception as err:
        #     print err
        local.current_request = request
        return None

    def process_response(self, request, response):
        if hasattr(local, 'current_request'):
            assert request is local.current_request
            del local.current_request

        return response

    def __call__(self, **kwargs):
        if not hasattr(local, 'current_request'):
            raise Exception(
                u"get_request can't be called in a new thread.")
        return local.current_request


def get_request():
    if hasattr(local, 'current_request'):
        return local.current_request
    else:
        raise Exception(u"get_request: current thread hasn't request.")


def get_x_request_id():
    x_request_id = ''
    http_request = get_request()
    if hasattr(http_request, 'META'):
        meta = http_request.META
        x_request_id = (meta.get('HTTP_X_REQUEST_ID', '')
                        if isinstance(meta, dict) else '')
    return x_request_id
