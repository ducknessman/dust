#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/25 20:19

import sqlite3
import os

class Connect(object):

    def __init__(self,db=None, cur=None):
        self.db = db
        self.cur = cur

    def __enter__(self, *args):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()
        self.cur.close()
        self.db.close()

class Sqlite(Connect):

    def __init__(self):
        basic = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        path = os.path.join(basic, 'data.sqlite')
        db = sqlite3.connect(path)
        cur = db.cursor()
        super(Sqlite, self).__init__(db, cur)