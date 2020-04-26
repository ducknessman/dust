#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/26 14:58

from collections import Counter
from itertools import chain
import demjson

def analysis_word_could(direction,response):
    infos = sum(list(combine_with_dict(direction,response)),[])
    count = Counter(infos)
    return dict(count)

def combine_with_dict(direction,response):
    for value1,value2 in zip(direction,response):
        info = unpack_tuple(value1,value2)
        yield list(info)

def unpack_tuple(value1,value2):
    if isinstance(value1,str) or isinstance(value2,str):
        return chain(sum(tuple(demjson.decode(value1).items()), ()), sum(tuple(demjson.decode(value2).items()), ()))
    else:
        return chain(sum(tuple(value1.items()),()),sum(tuple(value2.items()),()))