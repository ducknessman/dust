#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/23 13:13

import requests

class SingleRequest():

    def __init__(self,cookies=None,headers=None):
        types = dict([('json', 'application/json'),
                    ('file', 'multipart/form-data'),
                    ('data', 'application/x-www-form-urlencoded')])
        cookies = {} if cookies is None else cookies
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/81.0.4044.122 Safari/537.36'} if headers is None else headers

        self.types = types
        self.cookies = cookies
        self.headers = headers


    def choice_type(self,types):
        for key,value in self.types.items():
            if types == value:
                return "{}={}".format(key,{})


    def post(self,url,data):
        response = requests.post(url,data,cookies=self.cookies,headers=self.headers)
        return self.get_result(response)

    def get(self,url,data=None):
        data = {} if data == "" else data
        response = requests.get(url,params=data,cookies=self.cookies,headers=self.headers)
        return self.get_result(response)

    def put(self):
        pass

    def delete(self):
        pass

    def get_result(self,response):
        try:
            return response.json()
        except Exception as e:
            return {'code':response.status_code,'result':response.text[:200],'error':e}