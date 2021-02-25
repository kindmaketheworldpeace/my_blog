# -*- coding: utf-8 -*-
"""
校验装饰器单元
"""

import os
from functools import wraps

from django.http import JsonResponse
from django.utils.decorators import available_attrs
from django.core.exceptions import ValidationError


def size_mapper(size):
    """
    1G/1M/1K/1 --> 1024*1024*1024/1024*1024/1024/1Byte
    """

    if isinstance(size, int):
        return size
    else:
        size = size.lower()

    if size.endswith('g'):
        factor = 1024 * 1024 * 1024.0
    elif size.endswith('m'):
        factor = 1024 * 1024.0
    elif size.endswith('k'):
        factor = 1024.0
    else:
        raise ValidationError(u'格式错误，仅支持【G/M/K】结尾的大小标记字符串.')
    size = size.replace('g', '').replace('m', '').replace('k', '')
    return int(size) * factor


def validate_file_upload(max_size, content_types=None, file_exts=None):
    """
    文件上传校验，带参装饰器
        max_size: 单位G/M/K
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            upload_file = request.FILES.get('files[]')
            max_upload_size = size_mapper(max_size)

            # 文件大小校验
            if upload_file.size == 0:
                return JsonResponse({'code': 'FILE_NOT_ALLOWED', 'result': False, 'message': u'禁止上传空文件.'})
            elif upload_file.size > max_upload_size:
                return JsonResponse({'code': 'FILE_NOT_ALLOWED', 'result': False,
                                     'message': u'上传文件大小不得超过%s.' % max_size})

            # application/type， 对type进行白名单校验
            if content_types and upload_file.content_type.split('/')[-1] not in content_types:
                return JsonResponse({'code': 'FILE_NOT_ALLOWED', 'result': False,
                                     'message': u'上传文件类型仅支持：%s' % ', '.join(content_types)})

            # 对文件后缀进行白名单校验
            if file_exts and os.path.splitext(upload_file.name)[-1] not in file_exts:
                return JsonResponse({'code': 'FILE_NOT_ALLOWED', 'result': False,
                                     'message': u'上传文件类型仅支持：%s' % ', '.join(file_exts)})
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def validate_template(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def __wrapper(request, *args, **kwargs):
        """
        无参装饰器
        """

        return view_func(request, *args, **kwargs)

    return __wrapper


def validate_template_(param1, param2=None):
    """
    带参装饰器
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # do something with params
            print param1, param2

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
