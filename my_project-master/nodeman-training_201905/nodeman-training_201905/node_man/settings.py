# -*- coding: utf-8 -*-
import os
import posixpath
from django.conf import settings as _django_settings

####################################################################################################
# 首页配置
####################################################################################################


# INDEX_TEMPLATE = {
#     'DEVELOP': _django_settings.APP_ID + '/node_man/templates/index.html',
#     'TEST': _django_settings.APP_ID + '/test/index.html',
#     'PRODUCT': _django_settings.APP_ID + '/product/index.html',
# }.get(_django_settings.RUN_MODE)
#
INDEX_TEMPLATE = '/node_man/templates/index.html'


####################################################################################################
# 安装路径配置
####################################################################################################


def mkdir_if_not_exist(directory):
    """
    创建系统文件存储路径
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            pass


# 系统文件根路径
BASE_DIR = os.path.join(_django_settings.PROJECT_ROOT, 'USERRES')
mkdir_if_not_exist(BASE_DIR)

# 本地存放安装文件
TMP = '/tmp'
LOCAL_PATH = os.path.join(BASE_DIR, 'agents')
mkdir_if_not_exist(LOCAL_PATH)

# 本地存放密钥文件
LOCAL_KEY_PATH = os.path.join(BASE_DIR, 'keys')
mkdir_if_not_exist(LOCAL_KEY_PATH)

# 本地存放临时压缩包
ZIP_PATH = os.path.join(BASE_DIR, 'zips')
mkdir_if_not_exist(ZIP_PATH)

# 本地存放临时安装脚本
SCRIPT_DIR = os.path.join(BASE_DIR, 'scripts')
mkdir_if_not_exist(SCRIPT_DIR)

# 远程临时安装目录
REMOTE_PATH = posixpath.join(TMP, 'agents')
REMOTE_KEY_PATH = posixpath.join(TMP, 'keys')

####################################################################################################
# 加密配置
####################################################################################################
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDYvKQ/dAh499dXGDoQ2NWgwlev
GWq03EqlvJt+RSaYD1STStM6vEvsPiQ0Nc1GqxvZfqyS6v6acIbhCa1qgYKM8IGk
OVjmORwDUqVR807uCE+GXlf98PSxBbdAPp5e5dTLKd/ZSD6C70lUrMoa8mOktUp/
NnapTCnlIg0YdZjLVwIDAQAB
-----END PUBLIC KEY-----"""
RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----                     
MIICXQIBAAKBgQDYvKQ/dAh499dXGDoQ2NWgwlevGWq03EqlvJt+RSaYD1STStM6
vEvsPiQ0Nc1GqxvZfqyS6v6acIbhCa1qgYKM8IGkOVjmORwDUqVR807uCE+GXlf9
8PSxBbdAPp5e5dTLKd/ZSD6C70lUrMoa8mOktUp/NnapTCnlIg0YdZjLVwIDAQAB
AoGAUghMTmv3jPmZerCDwb6gVMFZ+L8xARVj94kEfW1k5ybeRwWKH3AHeHoor84x
TO8UkmR8ovrotMGke2ZzSZ2NMGJi9D4/hY9yEwKctPtYi6ve/2d2wDJcxRmd8zaW
k7eRJH5RUdGqNJWXp+MqaRwU6N+864UnuW59PSGSK5MXzrkCQQD7a+cZz1C1+4Zb
llhPFPxp59FhbBV4hU7fnvBPWOxBQN54kC6mRgbrlo9qe1U3NjQVFTzmtCQIoxZZ
4UDH+seNAkEA3K8LFQiZs+J8+odzVx3PWbR30EikKxAJsBRcepRdk8cKmMAWGahA
EzfGtKqEz2UpKPTwYvwCkBEbOlK9LCSDcwJBAMVaLp5Y2H7wv8dWnVz+GSA8gmNZ
hwUChyYLSZDPOSwDcl3qt2N3Jml41nx78SkUmA9Qi2yATKSm9513rfULyeUCQBYB
YmKDjAgS8pFsxkSOlWmFhFkBlVUx8TVcomgauUYOF/FpXgrK6zC/ZBIJ2tpvZO5P
llTYekzxV7y2GWT4cx8CQQDI41+oFsrycLX87TUCotISruNTuyXkqHeFvQqoum84
jiISOjFtfT9gz3aEmQiJmqgVg6/I3gDYhuB68GU6J/+g                    
-----END RSA PRIVATE KEY-----"""
