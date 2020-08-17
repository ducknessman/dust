#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/06 19:03

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import HttpServerApp
from exts import db
from app import models as admin_user

app = HttpServerApp()
manage = Manager(app)
Migrate(app,db)
manage.add_command('db',MigrateCommand)
@manage.option('-u','--username',dest='username')
@manage.option('-p','--password',dest='password')
@manage.option('-e','--email',dest='email')
@manage.option('-ph','--phone',dest='phone')
@manage.option('r', '--role' ,dest='role')
def create_user(username,password,email,phone,role):
    user_name = admin_user.User(username=username,password=password,email=email,phone=phone,role_id=role)
    db.session.add(user_name)
    db.session.commit()
    print('添加成功')

if __name__ == '__main__':
    manage.run()