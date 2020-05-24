#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/06 19:03

from flask import Flask
from .login import Login
from .admin import admin
from exts import db

def HttpServerApp():

    app = Flask(__name__)
    app.register_blueprint(Login)
    app.register_blueprint(admin)
    app.jinja_env.auto_reload = True
    app.config.from_object('setting.BasicConfig')
    db.init_app(app)

    @app.template_filter("split_path")
    def split_path(path):
        path_list = path.split('/')
        path_list = [[path_list[i - 1], '/'.join(path_list[:i])] for i in range(1, len(path_list) + 1)]
        return path_list

    return app