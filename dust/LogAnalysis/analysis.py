#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/20 11:45

import datetime
import os
from setting import BasicConfig as bc
from collections import Counter

def split_info(info,message):
    return info.split(message)

def collection_info(infos):
    try:
        _, info = split_info(infos, 'INFO -')
        info = info.replace('}"', "}")
        info = eval(info)
        yield info
    except Exception as e:
        pass

def count_info(fname):
    with open(fname) as fp:
        for info in split_info(fp.read(),'end_logs'):
            value = collection_info("".join(info.split('\n')))
            yield from value

def collection_words():
    word_could = {}
    real_name = 'query_logs_{}.log'.format(datetime.datetime.now().strftime('%Y_%m_%d'))
    fname = os.path.join(bc.BASIC_PATH,'logs',real_name)
    for name in count_info(fname):
        for key,value in name.items():
            word_could.setdefault(key,[]).append(value)
    use = map(lambda x:dict(Counter(x[1])),word_could.items())
    return real_name,dict([j for i in use for j in i.items()])