# -*- coding: utf-8 -*-

from component.utils.basic import (tuple_choices, choices_to_namedtuple)

CODE_STATUS_TUPLE = (
    'OK', 'UNAUTHORIZED', 'VALIDATE_ERROR', 'METHOD_NOT_ALLOWED',
    'PERMISSION_DENIED', 'SERVER_500_ERROR', 'OBJECT_NOT_EXIST')
CODE_STATUS_CHOICES = tuple_choices(CODE_STATUS_TUPLE)
ResponseCodeStatus = choices_to_namedtuple(CODE_STATUS_CHOICES)

# 常规字段长度定义
LEN_SHORT = 32
LEN_NORMAL = 64
LEN_MIDDLE = 128
LEN_LONG = 256
LEN_X_LONG = 1024
LEN_XX_LONG = 10240
LEN_XXX_LONG = 20480

# 字段默认值
EMPTY_INT = 0
EMPTY_STRING = ""
EMPTY_LIST = []
EMPTY_DICT = {}
DEFAULT_BK_BIZ_ID = -1
EMPTY = "EMPTY"


ROLE_CHOICES = [
    ("CMDB", u"CMDB业务公用角色"),
    ("GENERAL", u"通用角色表"),
    ("OPEN", u"不限"),
    ("PERSON", u"个人"),
    ("EMPTY", u"无"),
]

SCRIPT_CHOICES = [
    (1, "shell"),
    (2, "bat"),
    (3, "perl"),
    (4, "python"),
    (5, "powershell"),
]

TASK_STATUS_CHOICES = [
    (1, u"未执行"),
    (2, u"正在执行"),
    (3, u"执行成功"),
    (4, u"执行失败"),
    (13, u"已拒绝"),
    (14, u"待复核"),
    (15, u"待审批"),
]

JOB_STATUS_CHOICES = [
    (1, u"未执行"),
    (2, u"正在执行"),
    (3, u"执行成功"),
    (4, u"执行失败"),
    (5, u"跳过"),
    (6, u"忽略错误"),
    (7, u"等待用户"),
    (8, u"手动结束"),
    (9, u"状态异常"),
    (10, u"步骤强制终止中"),
    (11, u"步骤强制终止成功"),
    (12, u"步骤强制终止成功"),
]