# -*- coding: utf-8 -*-
import logging
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger('component')


class ServerError(Exception):
    """
        后台错误类
    """
    MESSAGE = _(u"系统异常")
    ERROR_CODE = 'FATAL_ERROR'

    def __init__(self, *args):
        self.code = self.ERROR_CODE
        self.message = u"%s: %s" % (self.MESSAGE, args[0]) if args else self.MESSAGE
        super(ServerError, self).__init__(*args)

    def __str__(self):
        return "<AppError %s:(%s)>" % (self.code, self.message)


class ParamError(ServerError):
    MESSAGE = _(u"参数验证失败")
    ERROR_CODE = 'FORM_VALIDATE_ERROR'


class PlatDoesNotExistError(ServerError):
    MESSAGE = _(u"云区域不存在")
    ERROR_CODE = 'PLAT_DOES_NOT_EXIST_ERROR'


class PlatCanNotDeleteError(ServerError):
    MESSAGE = _(u"删除失败")
    ERROR_CODE = 'PLAT_CAN_NOT_DELETE_ERROR'


class RemoteCallError(ServerError):
    MESSAGE = _(u"远程服务请求结果异常")
    ERROR_CODE = 'REMOTE_CALL_ERROR'


class ComponentCallError(ServerError):
    MESSAGE = _(u"组件调用异常")
    ERROR_CODE = 'COMPONENT_CALL_ERROR'

    def __init__(self, *args):
        """组件错误信息格式化"""
        if args:
            res = args[0]
            self.MESSAGE = u"%s:%s(code=%s)" % (self.MESSAGE, res.get('message'), res.get('code'))
            self.esb_response = args[0]

            try:
                self.esb_parameter = args[1]
            except IndexError:
                self.esb_parameter = ([], {})

            try:
                self.esb_api = args[2]
            except IndexError:
                self.esb_api = 'one_api'

            super(ComponentCallError, self).__init__()
        else:
            super(ComponentCallError, self).__init__(*args)

    def record_transaction(self, logger_func, *args, **kwargs):
        logs = ("ESB Component Error:",
                "ESB api: {}".format(self.esb_api),
                "request parameter: {}".format(self.truncate_esb_parameter()),
                "response: {}".format(str(self.esb_response)))
        logger_func(logs[1], *args, **kwargs)
        logger.error('\n'.join(logs))

    def truncate_esb_parameter(self):
        args, kwargs = self.esb_parameter
        args = [("{}...".format(arg[:47])) if (isinstance(arg, basestring) and len(arg) > 50) else arg
                for arg in args]
        kwargs = {k: ("{}...".format(v[:47])) if (isinstance(v, basestring) and len(v) > 50) else v
                  for k, v in kwargs.iteritems()}
        return str((args, kwargs))


class PermissionError(ServerError):
    MESSAGE = _(u"权限不足")
    ERROR_CODE = 'PERMISSION_ERROR'


class NginxSettingError(ServerError):
    MESSAGE = _(u"nginx配置信息不存在")
    ERROR_CODE = 'NGINX_SETTING_ERROR'


class GseSettingError(ServerError):
    MESSAGE = _(u"nginx配置信息不存在")
    ERROR_CODE = 'NGINX_SETTING_ERROR'


class NginxConnectionError(ServerError):
    MESSAGE = u"nginx connection error:"
    ERROR_CODE = 'NGINX_CONNECTION_ERROR'


class InitializeError(ServerError):
    """
        后台错误类
    """
    MESSAGE = _(u"初始化异常")
    ERROR_CODE = 'INIT_FAILURE'


class StepFailure(Exception):
    def __init__(self):
        self.message = "step failed"
        self.code = "STEP_FAILED"
