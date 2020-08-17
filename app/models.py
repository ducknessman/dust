#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/06 19:04

from datetime import datetime

from exts import db
from werkzeug.security import generate_password_hash,check_password_hash

# 用户表
class User(db.Model):
    '''
    _password:对内密码
    password:对外密码
    '''
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True) #用户id
    username = db.Column(db.String(100),nullable=False,unique=True) # 用户名
    _password = db.Column(db.String(500),nullable=False) # 密码
    email = db.Column(db.String(100),nullable=False,unique=True) # 邮箱
    phone = db.Column(db.String(20),unique=True) # 电话
    fullname = db.Column(db.String(100)) #全称
    status = db.Column(db.Integer)  # 状态
    is_super = db.Column(db.SmallInteger)  # 是否为管理员，1为管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    remarks = db.Column(db.String(500))  # 备注
    reg_time = db.Column(db.DateTime, default=datetime.now) #注册时间

    def __init__(self,username=None,password=None,email=None,phone=None,fullname=None,
                 status=None,is_super=None,role_id=None,remarks=None,reg_time=None):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.fullname = fullname
        self.status = status
        self.is_super = is_super
        self.role_id = role_id
        self.remarks = remarks
        self.reg_time = reg_time

    #获取密码
    @property
    def password(self):
        return self._password

    #设置密码
    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    #检查密码
    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

#测试用例
class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #记录id
    task_id = db.Column(db.String(100),nullable=False) #用例编号
    task_son_id = db.Column(db.String(200),unique=True,nullable=False) #用例子编号
    task_name = db.Column(db.String(500),nullable=False) # 用例名称
    task_description = db.Column(db.String(4096),nullable=False) # 用例描述
    task_url = db.Column(db.String(1024),nullable=False) # 用例地址
    task_method = db.Column(db.String(100),nullable=False) #请求方法
    task_data = db.Column(db.String(4096)) # 用例数据
    task_result = db.Column(db.String(4096),nullable=False) # 预期结果
    task_session = db.Column(db.Integer,nullable=False) #是否需要session ,0:不需要，1：需要
    sessions = db.Column(db.String(4096)) #登录session
    task_auth = db.Column(db.String(1024))  #用例执行人信息
    task_env = db.Column(db.Integer,nullable=False) #是否需要环境变量，0：不需要，1：stage，2：alpha，3：real
    task_time = db.Column(db.String(4096)) #添加时间

#测试环境变量
class Env(db.Model):
    __tablename__ = 'env'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 记录id
    env_name = db.Column(db.String(4096),nullable=False) # 环境变量名称
    env_single = db.Column(db.Integer,nullable=False) #0：不需要，1：stage，2：alpha，3：real
    env_url = db.Column(db.String(4096),nullable=False) # 环境变量地址
    description = db.Column(db.String(4096),nullable=False)# 环境描述

#测试报告
class TaskReport(db.Model):
    __tablename__ = 'taskreport'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 记录id
    report_name = db.Column(db.String(4096),nullable=False) # 报告名称
    success_count = db.Column(db.Integer,nullable=False) # 成功数量
    fail_count = db.Column(db.Integer,nullable=False) # 失败数量
    error_account = db.Column(db.Integer,nullable=False) # 错误数量
    finished_time = db.Column(db.String(100),index=True,default=datetime.now) #生成报告时间

#测试结果
class TaskResult(db.Model):
    __tablename__ = 'task_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 记录id
    task_id = db.Column(db.String(100),nullable=False)  # 用例编号
    task_son_id = db.Column(db.String(100),nullable=False) # 用例子编号
    task_url = db.Column(db.String(500),nullable=False) # 用例地址
    task_data = db.Column(db.String(1024)) # 用例数据
    task_result = db.Column(db.String(2048),nullable=False) #用例结果
    task_response = db.Column(db.String(4096),nullable=False) # 请求响应结果
    task_status = db.Column(db.Integer,nullable=False) #0:success,1:fail,2:error
    finished_time = db.Column(db.String(100),index=True,default=datetime.now) #执行用例结束时间

# 定义角色数据模型
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    description = db.Column(db.String(600))  # 角色描述
    auths = db.Column(db.String(600))  # 权限列表
    add_time = db.Column(db.String(100), index=True, default=datetime.utcnow)  # 添加时间
    admins = db.relationship("User", backref='role')


# 定义权限数据模型
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100),unique=True)  # 名称，不能重复
    url = db.Column(db.String(255))  # 地址
    add_time = db.Column(db.String(100), index=True, default=datetime.utcnow)  # 添加时间

#管理员登录日志
class AdminLog(db.Model):
    __tablename__ = "admin_log"  #定义表名
    id = db.Column(db.Integer,primary_key=True) #编号
    #定义外键 db.ForeignKey
    admin_id = db.Column(db.Integer,db.ForeignKey('user.user_id')) #所属管理员
    operate = db.Column(db.String(300))  # 操作行为
    ip = db.Column(db.String(100))  #登录IP
    time=db.Column(db.String(100))#时间戳
    add_time = db.Column(db.String(100),index=True,default=datetime.now) #登录时间 ，默认时间

#操作日志
class OperateLog(db.Model):
    __tablename__ = 'operate_log'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    # 定义外键 db.ForeignKey
    admin_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    operate = db.Column(db.String(600))  # 操作行为
    add_time = db.Column(db.String(100), index=True, default=datetime.now)  # 登录时间 ，默认时间

#任务执行表
class TaskRun(db.Model):
    __tablename__ = 'task_run'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True) #序列编号
    running_name = db.Column(db.String(100),nullable=False) #执行名称
    running_info = db.Column(db.String(1024),nullable=False) #执行的用例子编号
    create_time = db.Column(db.String(100),nullable=False) # 创建时间