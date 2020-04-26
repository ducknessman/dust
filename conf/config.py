#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/20 11:01

import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret'
    DB_HOST = '127.0.0.1'
    DB_USER = 'foobar'
    DB_PASSWD = 'foobar'
    DB_DATABASE = 'foobar'
    ITEMS_PER_PAGE = 15
    UPLOAD_FOLDER = '{}/app/templates/report/upload_file/'.format(basedir)
    THUMBNAIL_FOLDER = '{}/app/templates/report/upload_file/thumbnail/'.format(basedir)
    MAX_CONTENT_LENGTH = 100 * 1024 ** 2
    ALLOWED_EXTENSIONS = set(['gif', 'png', 'jpg', 'jpeg',  'xls', 'xlsx'])

    JWT_AUTH_URL_RULE = '/api/auth'
    PUBLIC_KEY = ''    
    PRIVATE_KEY = ''
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
