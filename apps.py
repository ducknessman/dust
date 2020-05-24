#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/06 19:03

from app import HttpServerApp

app = HttpServerApp()

if __name__ == '__main__':
    app.run(host='127.0.0.1',threaded=True,debug=True,port=5566)