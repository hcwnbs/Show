#!/usr/bin/env python3
#  _*_ coding: utf-8 _*_

PATH = "E:/Notes/python/Project/Django/Show/static/download/"

import datetime
import xlwt
import MySQLdb
import os
import xlrd


def export(host, user, password, dbname, table_name):
    conn = MySQLdb.connect(host, user, password, dbname, charset='utf8')
    cursor = conn.cursor()

    count = cursor.execute('select * from ' + table_name)
    # 重置游标的位置
    cursor.scroll(0, mode='absolute')
    # 搜取所有结果
    results = cursor.fetchall()

    # 获取MYSQL里面的数据字段名称
    fields = cursor.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_' + table_name, cell_overwrite_ok=True)

    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(results) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row - 1][col])
    da_path = "download/" + str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + '.xlsx'
    outputpath = PATH + str(datetime.datetime.now().year) + str(datetime.datetime.now().month) + str(datetime.datetime.now().day) + str(datetime.datetime.now().hour) + '.xlsx'
    if not os.path.exists(outputpath):
        workbook.save(outputpath)
    return da_path

def toSql(path):
    name = path.split('/')[-1]
    year, month, day = name[:4], name[4:5], name[5:7]
    return path, year, month, day

def getData():
    L_each = []
    L_each_full = []
    L_know = []
    data_dir = r"D:/用户目录/我的文档/WeChat Files/Yellow520hc/Files/2013DM2marks.xlsx"
    book = xlrd.open_workbook(data_dir)  # 得到Excel文件的book对象，实例化对象
    sheet0 = book.sheet_by_index(0)  # 通过sheet索引获得sheet对象

    cell = sheet0.row_values(1)[7:]
    for i in range(len(cell)):
        if i%2 == 0:
            L_know.append(cell[i]) #每个小题知识点

    cell_value = sheet0.col_values(6)
    L_full = cell_value[3:]  #总分

    L_eachfull = sheet0.row_values(3)[7:]
    for i in range(len(L_eachfull)):
        if i%2 != 0:
            L_each_full.append(L_eachfull[i]) #每个小题满分值

    nrows = sheet0.nrows
    for i in range(3, nrows):
        temp = []
        L_eachs = sheet0.row_values(i)[7:]
        for j in range(len(L_eachs)):
            if j%2 == 0:
                temp.append(L_eachs[j])
        L_each.append(temp) #每个小题得分

    data = [L_know, L_each, L_each_full, L_full]
    return data


# 结果测试
if __name__ == "__main__":
    # export('localhost', 'root', 'hcwnbs', 'show', 'data', PATH + 'datetest.xlsx')

   print(getData()[3])