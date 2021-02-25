# -*- coding: utf-8 -*-
"""
    前端加密参考：
    http://travistidwell.com/jsencrypt/
    https://github.com/travist/jsencrypt

    TODO：待确认
    https://gist.github.com/ficapy/8fa6b37265d5394dd7a4
    >> #  以下RSA加密解密做法官方不推荐使用(至于为什么不安全我也不造)
    key = RSA.importKey(pub).encrypt('xxxx', 'x')  # 第二个参数没有用处  只是为了兼容性
    print RSA.importKey(pri).decrypt(key)
"""
import rsa
import base64

from common.log import logger
from node_man.settings import RSA_PRIVATE_KEY, PUBLIC_KEY


def rsa_encrypt(message):
    """
    RSA加密
    """
    return base64.b64encode(rsa.encrypt(
        str(message),
        rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY)
    ))


def rsa_decrypt(encrypted):
    """
    RSA解密
    """
    return rsa.decrypt(
        base64.decodestring(encrypted),
        rsa.PrivateKey.load_pkcs1(RSA_PRIVATE_KEY)
    )


if __name__ == '__main__':
    # 加解密测试
    message = "Bk@170921yy"
    encrypted = rsa_encrypt(message)
    decrypted = rsa_decrypt(encrypted)
    print encrypted, decrypted == message, message
    # 前端加密后的内容：
    # encrypted = "H7lkjMm7R3S/9jPjB7YSAMM7o4oTasnIXi7z0oYBDqXggn9V/Q0yK580ToaeyP8KG4inTFvgQ2nzYxWXTFDSfj" \
    #             "vNKCyOMU2cRYPt3pSm3BW2OHCKWjnsWoaCGAe66uNvCu2QyGCE+ds6gTVltlzbvFc4NcBlAvYSrHil6D99k7E="
    # decrypted = rsa_decrypt(encrypted)
    # print encrypted, decrypted == message, message
