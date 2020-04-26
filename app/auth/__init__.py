#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
