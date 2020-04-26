#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/24 16:41

import hmac, base64, struct, hashlib, time

def calGoogleCode(secretKey):
    try:
        input = int(time.time()) // 30
        key = base64.b32decode(secretKey.upper().replace(" ", ''))
        msg = struct.pack(">Q", input)
        googleCode = hmac.new(key, msg, hashlib.sha1).digest()
        o = googleCode[19] & 15
        googleCode = str((struct.unpack(">I", googleCode[o:o + 4])[0] & 0x7fffffff) % 1000000)
        if len(googleCode) == 5:  
            googleCode = '0' + googleCode
        return googleCode
    except Exception as e:
        return {0:e}