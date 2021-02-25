# -*- coding: utf-8 -*-
"""Login middleware."""

from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import get_token as get_csrf_token

from account.accounts import Account

User = get_user_model()


class AutoLoginMiddleware(object):
    """
        Auto Login middleware.
        为了应对不稳定的PaaS联调环境
    """

    def process_view(self, request, view, args, kwargs):
        """process_view."""
        request.user = User.objects.get(pk=1)
        return None


class LoginMiddleware(object):
    """Login middleware."""

    def process_view(self, request, view, args, kwargs):
        """process_view."""
        if getattr(view, 'login_exempt', False):
            return None
        user = authenticate(request=request)
        if user:
            request.user = user
            get_csrf_token(request)
            return None

        account = Account()
        return account.redirect_login(request)


class DisableCSRFCheck(object):
    """本地开发，去掉django rest framework强制的csrf检查
    """

    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return None


class GateWayIgnoreFCheck(object):

    def process_request(self, request):
        # Todo: remove me
        setattr(request, '_dont_enforce_csrf_checks', True)

        if request.path.find("/gateway/") >= 0:
            setattr(request, '_dont_enforce_csrf_checks', True)
            setattr(request, '_login_exempt', True)
        return None

    def process_view(self, request, view, args, kwargs):
        """process_view."""
        if getattr(request, '_login_exempt', False):
            setattr(view, 'login_exempt', True)
        return None
