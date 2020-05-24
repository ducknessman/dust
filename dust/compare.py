#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/17 10:48

import difflib
import json
from collections import Counter

class Compare:

    def judge_type(self,result,response):
        if isinstance(response,str):
            return self.compare_str(result,response)

        if isinstance(response,dict):
            return self.compare_json(result,response)

    def compare_json(self,result,response):
        single_result = []
        try:
            result = json.loads(result)
        except Exception as e:
            self.compare_str(str(result),str(response))
        for key,value in result.items():
            try:
                if response[key] == value:
                    single_result.append('success')
                else:
                    single_result.append('fail')
            except KeyError as e:
                return 'fail'
        else:
            finall_result = dict(Counter(single_result))
            if len(finall_result.keys()) == 1 and finall_result['success'] != 0:
                return 'success'
            elif len(finall_result.keys()) == 1 and finall_result['fail'] != 0:
                return 'fail'
            else:
                return 'fail'



    def compare_str(self,result,response,num=0.75):
        percent = difflib.SequenceMatcher(None, result,response).quick_ratio()
        if 'error' in response:
            return 'error'
        elif percent > num:
            return 'success'
        else:
            return 'fail'