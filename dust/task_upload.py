#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/05/17 20:49

import xlrd

import json
import datetime
from itertools import product

class UploadExcel:

    def __init__(self,filename):
        self.path_name = filename

    def read_excel(self):
        work_book = xlrd.open_workbook(self.path_name)
        sheets_name = work_book.sheet_names()
        for sheet_name in sheets_name:
            title, value = [], []
            work_sheet = work_book.sheet_by_name(sheet_name)
            rows = work_sheet.nrows
            cols = work_sheet.ncols
            for row,col in product(range(0,rows),range(cols)):
                if row == 0:
                    title.append(work_sheet.cell(row,col).value)
                if (col == 0 or col == 9 or col == 10) and row > 0:
                    value.append(int(work_sheet.cell(row,col).value))
                elif col == 6 and row > 0:
                    if work_sheet.cell(row,col).value == '':
                        value.append("{}")
                    else:
                        value.append(work_sheet.cell(row, col).value)
                elif col == 3 and row > 0:
                    value.append((work_sheet.cell(row, col).value).upper())
                elif col == 8 and row > 0:
                    value.append(work_sheet.cell(row, col).value)
                elif row > 0:
                    value.append(work_sheet.cell(row, col).value)
            yield from self.combine_dict(title,value)

    def combine_dict(self,title,value):
        for i in range(0,len(value),12):
            single_task = dict(zip(title,value[i:i+12]))
            single_task['task_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            yield single_task

if __name__ == '__main__':
    st = UploadExcel('D:\\python_project\\dust-master\\uploade_data\\demo.xlsx')
    print(list(st.read_excel()))