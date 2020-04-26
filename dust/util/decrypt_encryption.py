#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/24 10:44

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkce_v1_5
import base64
import hashlib


def decrypt(private,cipher_text):
    try:
        private_key = '-----BEGIN RSA PRIVATE KEY-----\n'+ private + '\n-----END RSA PRIVATE KEY-----\n'
        res_key = RSA.importKey(private_key)
        cipher = Cipher_pkce_v1_5.new(res_key)
        info = cipher.decrypt(base64.b64decode(cipher_text),'ERROR')
        return info
    except Exception as e:
        return {0:e}


def encryption(public,password):
    try:
        public_key = """-----BEGIN PUBLIC KEY-----""" + '\n' + public + '\n' + """-----END PUBLIC KEY-----"""
        len_public_key = len(public)
        pub_body = Cipher_pkce_v1_5.new(RSA.importKey(public_key))
        if len_public_key < 245:
            encry_text = base64.b64encode(pub_body.encrypt(password.encode("utf-8")))
            encry_value = encry_text.decode("utf-8")
            return encry_value
               offset = 0
        res = []
        while len_public_key - offset > 0:
            if len_public_key - offset > 245:
                res.append(base64.b64encode(pub_body.encrypt(password.encode("utf-8")[offset:offset + len_public_key])).decode("utf-8"))
            else:
                res.append(base64.b64encode(pub_body.encrypt(password.encode("utf-8")[offset:])).decode("utf-8"))
            offset += len_public_key
        return "".join(res)
    except Exception as e:
        return {0:e}
        
def md5_dec(password):
    try:
        h = hashlib.md5()
        h.update(password.encode(encoding='utf-8'))
        new = h.hexdigest()
        return new
    except Exception as e:
        return {0:e}
