#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/26 10:14

import xlrd
import xlwt
from itertools import product

from conf.config import Config

class ControlExcel:

    def __init__(self,filename):
        base = Config.UPLOAD_FOLDER
        self.file_path = "{}{}".format(base,filename)

    def read_excel(self):
        work_book = xlrd.open_workbook(self.file_path)
        sheets_name = work_book.sheet_names()
        info = []
        for sheet_name in sheets_name:
            values = []
            work_sheet = work_book.sheet_by_name(sheet_name)
            rows = work_sheet.nrows
            cols = work_sheet.ncols
            for row,col in product(range(1,rows),range(cols)):
                if row > 0 and col == 0:
                    values.append(int(work_sheet.cell(row,col).value))
                elif row > 0 and 0<col<7:
                    values.append(work_sheet.cell(row, col).value)
                elif col == 7 and row>0:
                    values.append(work_sheet.cell(row, col).value)

            for index in range(0,len(values),8):
                info.append(values[index:index+8])
        return info

    def write_excel(self):
        pass





if __name__ == '__main__':
    print(list(ControlExcel('测试用例.xlsx').read_excel()))