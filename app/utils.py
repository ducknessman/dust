#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

import html
import json
import datetime
from urllib.parse import unquote
from dust.util.single_requests import SingleRequest
from dust.running_tasks.send_requests import SendRequests
from dust.running_tasks.report_demo import create_report
from dust.util.connect import Sqlite
from flask import Response, flash

def str_to_dict(dict_str):
    if isinstance(dict_str, str) and dict_str != '':
        new_dict = json.loads(dict_str)
    else:
        new_dict = ""
    return new_dict

def urldecode(raw_str):
    return unquote(raw_str)


def html_unescape(raw_str):
    return html.unescape(raw_str)
    
def kvstr_to_jsonstr(kvstr):
    kvstr = urldecode(kvstr)
    kvstr_list = kvstr.split('&')
    json_dict = {}
    for kvstr in kvstr_list:
        key = kvstr.split('=')[0]
        value = kvstr.split('=')[1]
        json_dict[key] = value
    json_str = json.dumps(json_dict, ensure_ascii=False, default=datetime_handler)
    return json_str


def dict_to_obj(dict, obj, exclude=None):
    for key in dict:
        if exclude:
            if key in exclude:
                continue
        setattr(obj, key, dict[key])
    return obj


def obj_to_dict(obj, exclude=None):
    dict = obj.__dict__['__data__']
    if exclude:
        for key in exclude:
            if key in dict: dict.pop(key)
    return dict


def query_to_list(query, exclude=None):
    list = []
    for obj in query:
        dict = obj_to_dict(obj, exclude)
        list.append(dict)
    return list

def running_task(env, query, exclude=None):
    infos = query_to_list(query, exclude=None)
    point = datetime.datetime.now()
    results = SendRequests().send_request(infos,cookies=env)
    success,fail,error,result = results
    with Sqlite() as db:
        sql = 'INSERT INTO report ("task_name","report_id","success_count","fail_count","error_count","finish_time") ' \
              'VALUES ("{}","{}",{},{},{},"{}") '.format(point.strftime("%Y%m%d%H%M%S"),point.strftime("%Y%m%d%H%M%S"),success,fail,error,point.strftime("%Y-%m-%d %H:%M:%S"))
        db.execute(sql)
    create_report(point.strftime("%Y%m%d%H%M%S"),point.strftime("%Y%m%d%H%M%S"),*results)
    return "测试结束，报告以生成"

def jsonresp(jsonobj=None, status=200, errinfo=None):
    if status >= 200 and status < 300:
        jsonstr = json.dumps(jsonobj, ensure_ascii=False, default=datetime_handler)
        return Response(jsonstr, mimetype='application/json', status=status)
    else:
        return Response('{"errinfo":"%s"}' % (errinfo,), mimetype='application/json', status=status)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Unknown type")


def form_to_model(form, model):
    for wtf in form:
        model.__setattr__(wtf.name, wtf.data)
    return model

def excel_to_model(excel):
    with Sqlite() as db:
        sql = 'INSERT INTO task ("task_id","task_son_id","task_url","task_method","task_name","task_data","auth_name","task_future_result") ' \
              'VALUES (?,?,?,?,?,?,?,?) '
        db.executemany(sql,excel)

def form_to_model_special(form, model):
    info = {}
    for wtf in form:
        info[wtf.name] = wtf.data or ""
    cookies = {} if info['cookies'] == "" else dict([value.split(":") for value in info['cookies'].split(',') ])
    headers = {} if info['header'] == "" else dict([value.split(":") for value in info['headers'].split(',') ])
    data = {} if info['data'] == "" else  dict([value.split(":") for value in info['data'].split(',') ])
    res = SingleRequest(cookies,headers)
    if info['task_method'] in ['POST','post']:
        result = res.post(info['task_url'],data)
    elif info['task_method'] in ['GET','get']:
        result = res.get(info['task_url'],data)
    elif info['task_method'] in ['PUT', 'put']:
        result = ''
    elif info['task_method'] in ['DELETE', 'delete']:
        result = ''

    if info['status']:
        point = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        temp = {'task_id':point,'task_son_id':"{}_1".format(point),'task_data':data,'task_future_result':result}
        model_value = {**info,**temp}
        for key,value in model_value.items():
            model.__setattr__(key,value)
        return result,model
    else:
        return result,0

def model_to_form(model, form):
    dict = obj_to_dict(model)
    form_key_list = [k for k in form.__dict__]
    for k, v in dict.items():
        if k in form_key_list and v:
            field = form.__getitem__(k)
            field.data = v
            form.__setattr__(k, field)


def flash_errors(form,err=None,file=None):
    if err:
        try:
            name = getattr(form, file).label.text
        except Exception as e:
            name = getattr(form, file).args
        flash("字段 [%s] 格式有误,错误原因: %s" % (
            name,
            err
        ))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("字段 [%s] 格式有误,错误原因: %s" % (
                    getattr(form, field).label.text,
                    error
                ))
