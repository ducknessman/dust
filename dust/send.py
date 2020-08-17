#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/16 18:46

import requests
import json
import html

class Request:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    def request(self,method,url,data,cookies,header=None,timeout=10):
        header = {**self.headers,**header} if header else self.headers
        data = {} if data in ["","{}"] else json.loads(data.replace('“','"').replace('”','"'))
        if cookies == 0:
            info = self.send(requests,method,url,data,cookies={},header=header)
        elif cookies == 1:
            res = requests.Session()
            info = self.send(res,method,url,data,cookies,header,timeout)
        return info


    def send(self,res,method,url,data,cookies=None,header=None,timeout=10):
        if method == "GET":
            response = res.request(method,url,params=data,headers=header,timeout=timeout)
            try:
                return response.json()
            except Exception as e:
                return html.unescape(response.text[:300])
        elif method == "POST":
            response = res.request(method,url,data=data,cookies=cookies,headers=header,timeout=timeout)
            try:
                return response.json()
            except Exception as e:
                return html.unescape(response.text[:300])