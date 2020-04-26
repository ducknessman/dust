#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/16 17:34

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, SqliteDatabase
import json
import random
from flask_login import UserMixin
from app import login_manager
from conf.config import config

import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']


# db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)
db = SqliteDatabase('{}/{}'.format(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),'data.sqlite'))

class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self.__data__.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


class User(UserMixin, BaseModel):
    username = CharField()  
    password = CharField()  
    fullname = CharField() 
    email = CharField()  
    phone = CharField()  
    status = BooleanField(default=True)  
    
class Auth(UserMixin, BaseModel):
    auth_name = CharField()
    username = CharField()  
    password = CharField() 
    googlecode = CharField()  


class Task(BaseModel):
    task_id = CharField()
    task_son_id = CharField()
    task_url = CharField()
    task_method = CharField()
    task_name = CharField()
    task_data = CharField()
    auth_name = CharField()
    task_future_result = CharField()


class TaskResult(BaseModel):
    task_id = CharField()
    task_name = CharField()
    describe = CharField()
    response = CharField()
    running_time = CharField()


class Report(BaseModel):
    task_name = CharField()
    report_id = CharField()
    success_count = CharField()
    fail_count = CharField()
    error_count = CharField()
    finish_time = CharField()


@login_manager.user_loader
def load_user(user_id):
    #User.id == int(user_id)
    # return User.get(True)
    return User.get(User.id == int(user_id))



def create_table():
    db.connect()
    db.create_tables([CfgNotify, User,Task,TaskResult,Report,Auth])
    admin_data = [{'username':'admin','password':'admin',
                   'fullname':'superadmin','email':'123456@qq.com',
                   'phone':'123456789','status':0}]
    # User().insert_many(admin_data).execute()
    tasks_data = [{'task_id':1,'task_son_id':'1-1','task_url':'http://www.baidu.com','task_method':'GET',
                   'task_name':'冒烟测试','task_data':"","auth_name":"zhuxx",'task_future_result':'200'},
                  {'task_id': 1, 'task_son_id': '1-2', 'task_url': 'http://www.baidu.com.123', 'task_method': 'GET',
                   'task_name': '冒烟测试', 'task_data': "","auth_name":"zhuxx", 'task_future_result': '500'},
                  {'task_id': 1, 'task_son_id': '1-3', 'task_url': 'https://www.baidu.com', 'task_method': 'GET',
                   'task_name': '冒烟测试', 'task_data': "","auth_name":"zhuxx", 'task_future_result': '200'},
                  ]
    # Task().insert_many(tasks_data).execute()
    report_data = [{'task_name':"冒烟测试-1",'report_id':"1",'success_count':50,
                    'fail_count':10,'error_count':3,'finish_time':"2020-04-20 15:20:32"},
                   {'task_name': "冒烟测试-2", 'report_id': "1", 'success_count': 50,
                    'fail_count': 10, 'error_count': 3, 'finish_time': "2020-04-20 15:20:32"},
                   {'task_name': "冒烟测试-3", 'report_id': "1", 'success_count': 50,
                    'fail_count': 10, 'error_count': 3, 'finish_time': "2020-04-20 15:20:32"}
                   ]
    # Report().insert_many(report_data).execute()
    print('{code:%s,result:%s}'%(random.choice([200,404,301,500]),1))
    task_result = [{"task_id":"2",'task_name':"冒烟测试-1",'describe':'{code:%s,result:%s}'%(random.choice([200,404,301,500]),i),
                    'response':'{code:%s,result:%s}'%(random.choice([200,404,301,500]),i),
                    "running_time":"2020-04-20 15:32:20"} for i in range(87)]
    TaskResult.insert_many(task_result).execute()

if __name__ == '__main__':
    create_table()