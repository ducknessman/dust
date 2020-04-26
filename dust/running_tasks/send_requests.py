#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/25 17:26

import difflib
import datetime

from dust.util.single_requests import SingleRequest
from dust.util.login import Login
from dust.util.connect import Sqlite

class SendRequests:

    def __init__(self):
        self.success = 0
        self.fail = 0
        self.error = 0

    def get_cookies(self,env,auth):
        cookies = Login(env,auth).login_step_2()
        return cookies

    def insert_task_result(self,value):
        with Sqlite() as db:
            sql = '''insert into taskresult ('task_id','task_name','describe','response','running_time') values (?,?,?,?,?)'''
            db.executemany(sql,[value,])

    def send_request(self,infos,cookies=None,header=None):
        results = []
        cookies = {} if cookies=='common' else self.get_cookies(cookies,infos['auth_name'])
        res = SingleRequest(cookies,header)
        for info in infos:
            if 'None' in info['task_data'] or info['task_data'] == '':
                data = {}
            else:
                data = eval(info['task_data'])

            if info['task_method'] == "POST":
                response = res.post(info['task_url'],data)
            elif info['task_method'] == "GET":
                response = res.get(info['task_url'],data)
            elif info['task_method'] == "PUT":
                response = 'the function is not used'
            else:
                response = 'the function is not used'

            result = self.judge_info(response,info)
            results.append(result)
            value = [info['task_id'],
                                    "{}_{}_{}".format(info['task_name'],info['task_id'],info['task_son_id']),
                                    str(info['task_future_result']),
                                    str(response),
                                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')]
            self.insert_task_result(value)
        return [self.success,self.fail,self.error,results]

    def judge_info(self,response, info):
        if isinstance(response,dict):
            result = self.check_json(info['task_future_result'],response)
            return self.judge(result, info, response)
        if isinstance(response,str):
            result = self.check_str(info['task_future_result'],response)
            return self.judge(result,info,response)

    def check_str(self,original,real,num=0.75):
        percent = difflib.SequenceMatcher(None, real, original).quick_ratio()
        if "ERROR" in real or "Error" in real:
            return 2
        elif percent > num:
            return 0
        else:
            return 1

    def check_json(self,original,real):
        if isinstance(original,str):
            return self.check_str(original,real,0.35)
        else:
            temp_success,temp_fail = 0,0
            for key,value in original.items():
                try:
                    if value == real[key]:
                        temp_success += 1
                    else:
                        temp_fail += 1
                except Exception as e:
                    temp_fail += 1
            if temp_success/sum(temp_fail,temp_success) >= 0.98:
                return 0
            elif 0.35 < temp_success/sum(temp_fail,temp_success) < 0.98:
                return 1
            else:
                return 2

    def judge(self,result,info,response):
        if result == 0:
            self.success += 1
            return (0,
                    '{}-{}-{}'.format(info['task_id'], info['task_son_id'], info['task_name']),
                    'the task_case is pass !! the url is {} nad data is {}'.format(info['task_url'], info['task_data']),
                    "the real response is {} ,the original is {}".format(response, info['task_future_result']))
        elif result == 1:
            self.fail += 1
            return (1,
                    '{}-{}-{}'.format(info['task_id'], info['task_son_id'], info['task_name']),
                    'the task_case is fail !! the url is {} nad data is {}'.format(info['task_url'], info['task_data']),
                    "the real response is {} ,the original is {}".format(response, info['task_future_result']))
        else:
            self.error += 1
            return (2,
                    '{}-{}-{}'.format(info['task_id'], info['task_son_id'], info['description']),
                    'error !! please check it,and retry!the url is {} and data is {}'.format(info['task_url'],
                                                                                             info['task_data']),
                    response['error'])