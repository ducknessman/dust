#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/06 19:07

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify

from app.models import User,AdminLog
from exts import db

import datetime


Login = Blueprint('login',__name__)

@Login.route('/')
def index():
    return redirect(url_for('login.login'))

@Login.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        username = User.query.filter_by(username=user).first()
        if user and pwd:
            if username:
                session['user_id'] = username.user_id
                if username.check_password(pwd):
                    op_log = AdminLog(
                        admin_id=username.user_id,
                        ip=request.remote_addr,
                        time=datetime.datetime.now(),
                        operate="用户：{} 进行了登录操作！".format(username.username)
                    )
                    db.session.add(op_log)
                    db.session.commit()
                    return jsonify({'code':200,'error':""})
                else:
                    print('用户名或密码错误')
                    return jsonify({'code':401,'error':'用户名或密码错误'})
            else:
                return jsonify({'code':401,'error':'用户名或密码错误'})
        else:
            return jsonify({'code': 401, 'error': '用户名或密码不能为空'})

@Login.route('/logout')
def logout():
    users = User.query.filter(User.user_id==session['user_id']).first()
    op_log = AdminLog(
        admin_id=users.user_id,
        ip=request.remote_addr,
        time=datetime.datetime.now(),
        operate="用户：{} 进行了注销操作！".format(users.username)
    )
    db.session.add(op_log)
    db.session.commit()
    del session['user_id']
    return redirect(url_for('login.login'))