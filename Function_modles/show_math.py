#!/usr/bin/env python3
#  _*_ coding: utf-8 _*_
import math
import numpy as np
import Function_modles.excel


all_list= [20, 20, 15, 15, 10, 10, 10, 100]

# 难度
def Nandu(data_list):
    all = [0, 0, 0, 0, 0, 0, 0]
    num = 0
    nandu = []
    for data in data_list:
        num = num + 1
        for i in range(0, len(data)-1):
            all[i] = all[i] + data[i]
    for j in range(0, len(all)):
        nandu.append(round((1 - (all[j]/num)/all_list[j]), 2))

    return nandu

# 区分度
def Qufendu(data_list):
    qufendu = []
    data_list = np.array(data_list)
    data_list = data_list[np.lexsort(data_list.T)]
    num = len(data_list)
    temp = (num*27)//100
    all_H = [0, 0, 0, 0, 0, 0, 0]
    all_L = [0, 0, 0, 0, 0, 0, 0]
    for data in data_list[:temp]:
        for i in range(0, len(data)-1):
            all_L[i] = all_L[i] + data[i]
    for data in data_list[-temp:]:
        for i in range(0, len(data) - 1):
            all_H[i] = all_H[i] + data[i]
    for j in range(0, len(all_H)):
        qufendu.append(round(((all_H[j]-all_L[j])/num)/all_list[j],2))
    return qufendu

# 未及率
def Weijilv(data_list):
    weijilv = []
    num = 0
    all = [0, 0, 0, 0, 0, 0, 0]
    for data in data_list:
        num = num + 1
        for i in range(0, len(data)-1):
            if data[i] == 0:
                all[i] = all[i] + 1

    for j in range(0, len(all)):
        weijilv.append(round(all[j]/num, 2))
    return weijilv
# 信度
def Xindu(data_list):
    xindu = []
    data_list = np.array(data_list)
    data_list = data_list[np.lexsort(data_list.T)]
    num = len(data_list)
    temp = (num * 27) // 100
    all_H = [0, 0, 0, 0, 0, 0, 0]
    all_L = [0, 0, 0, 0, 0, 0, 0]
    for data in data_list[:temp]:
        for i in range(0, len(data) - 1):
            all_L[i] = all_L[i] + data[i]
    for data in data_list[-temp:]:
        for i in range(0, len(data) - 1):
            all_H[i] = all_H[i] + data[i]
    for j in range(0, len(all_H)):
        xindu.append(round(((all_H[j] - all_L[j]) / num) / all_list[j], 2))
    return xindu


# 效度
def Xiaodu(data_list):
    xiaodu = []
    num = 0
    all = [0, 0, 0, 0, 0, 0, 0]
    for data in data_list:
        num = num + 1
        for i in range(0, len(data) - 1):
            if data[i] == 0:
                all[i] = all[i] + 1

    for j in range(0, len(all)):
        xiaodu.append(round(all[j] / num, 2))
    return xiaodu

# 及格率 及格人数
def Jigelv(data):
    num = 0
    for i in data:
        if i >= 60:
            num = num + 1
    return str(round((num/len(data)*100), 2)) + '%', num

# 平均分
def Pingjunfen(data):
    num = 0
    for i in data:
        num = num + i
    return round((num/len(data)), 2)

# 最高分
def Zuigaofen(data):
    num = 0
    for i in data:
        if i > num:
            num = i
    return num

# 各分段人数
def Fenduan(data):
    fenduan = [0, 0, 0, 0, 0]
    for i in data:
        if i < 60:
            fenduan[0] = fenduan[0] + 1
        elif i >= 60 and i < 70:
            fenduan[1] = fenduan[1] + 1
        elif i >= 70 and i < 80:
            fenduan[2] = fenduan[2] + 1
        elif i >= 80 and i < 90:
            fenduan[3] = fenduan[3] + 1
        elif i >= 90 and i <= 100:
            fenduan[4] = fenduan[4] + 1
    fenduannum = [fenduan[0], fenduan[1], fenduan[2], fenduan[3], fenduan[4]]
    fenduan[0] = round(fenduan[0]/len(data)*100, 2)
    fenduan[1] = round(fenduan[1]/len(data)*100, 2)
    fenduan[2] = round(fenduan[2]/len(data)*100, 2)
    fenduan[3] = round(fenduan[3]/len(data)*100, 2)
    fenduan[4] = round(fenduan[4]/len(data)*100, 2)
    return fenduan, fenduannum

if __name__ == '__main__':
    # 测试
    data = Function_modles.excel.getData()[3]
    print(Jigelv(data), Pingjunfen(data), Fenduan(data), Zuigaofen(data))


