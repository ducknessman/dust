#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.select()
            for single in user:
                if single.username == form.username.data and single.password == form.password.data:
                    login_user(single, form.rememberme.data)
                    return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('用户名或密码错误')
        except:
            flash('用户名或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('auth.login'))
