#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from conf.config import config
import logging
from logging.config import fileConfig
import os

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
# fileConfig('conf/log-app.conf')

def get_logger(name):
    return logging.getLogger(name)


def get_basedir():
    return os.path.abspath(os.path.dirname(__file__))


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    config[config_name].init_app(app)

    login_manager.init_app(app)
    bootstrap = Bootstrap(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
