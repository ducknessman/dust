#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/08 09:56

from wtforms import Form
from wtforms import StringField, PasswordField,BooleanField # 导入用到的字段
from wtforms.validators import InputRequired,DataRequired,EqualTo,Length,ValidationError

class AddTask(Form):
    task_id = StringField()
    task_son_id = StringField()
    task_name = StringField()
    task_description = StringField()
    task_url = StringField()
    task_method = StringField()
    task_data = StringField(default='')
    task_result = StringField()
    task_session = StringField(default=0)
    task_auth = StringField()
    task_env = StringField(default=0)
    sessions = StringField(default='')
    task_time = StringField()

class AuthForm(Form):
    name = StringField()
    url = StringField()
    add_time = StringField()

class RoleForm(Form):
    name = StringField()
    description = StringField()
    auths = StringField()
    add_time = StringField()

class UserForm(Form):
    username = StringField()
    password = StringField()
    email = StringField()
    phone = StringField()
    fullname = StringField()
    status = StringField()
    role_id = StringField()
    remarks = StringField()
    reg_time = StringField()

class TaskRunning(Form):
    running_name = StringField()
    running_info = StringField()
    create_time = StringField()