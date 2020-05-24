#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/06 19:04

import os

class BasicConfig:
    BASIC_PATH = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = '123456789'                                                  
    #mysql 数据库
    DB_USERNAME = 'root'
    DB_PASSWORD = 'root'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'dust'
    # DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
    # sqllite
    DB_URL = 'sqlite:///' + os.path.join(BASIC_PATH, 'data.sqlite')+'?check_same_thread=False'     

    SQLALCHEMY_DATABASE_URI = DB_URL                                            
    SQLALCHEMY_TRACK_MODIFICATIONS = False                                      
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_RECORD_QUERISE = True

    FLASK_DB_QUERY_TIMEOUT = 0.5

    UPLOAD_FOLDER = '{}/{}'.format(BASIC_PATH,'uploade_data')
    MAX_CONTENT_LENGTH = 16 * 1024 ** 3
    ALLOWED_EXTENSIONS = set(['xls','xlsx'])

