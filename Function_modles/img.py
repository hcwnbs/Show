#!/usr/bin/env python3
#  _*_ coding: utf-8 _*_
from numpy import *
from PIL import Image, ImageDraw
from os import listdir
from Function_modles import knn, kmeans
import shutil

import os, sys

BASE_DIR = 'E:/Notes/python/Project/Django/Show/upload/'
TO_DIR = 'E:/Notes/python/Project/Django/Show/static/upload/'

# 图像二值化
def toBlack(fileName):
    im = Image.open(fileName).convert('L')
    pixels = im.load()
    for x in range(im.width):
        for y in range(im.height):
            pixels[x, y] = 255 if pixels[x, y] > 125 else 0
    im.save(fileName)

# 定位成绩位置
def locate(fileName):
    im = Image.open(fileName)
    img1 = im.crop((800, 913, 1236, 1039))
    img2 = im.crop((1300, 913, 1752, 1039))
    img3 = im.crop((1800, 915, 2262, 1045))
    img4 = im.crop((2303, 921, 2769, 1047))
    img5 = im.crop((2804, 921, 3272, 1049))
    img6 = im.crop((4329, 921, 4805, 1047))
    files = fileName[:-4]
    if not os.path.exists(files):
        os.mkdir(files)
    img1.save(files + '/'+ files[-1] +'_1' + '.png')
    img2.save(files + '/'+ files[-1] +'_2' + '.png')
    img3.save(files + '/'+ files[-1] +'_3' + '.png')
    img4.save(files + '/'+ files[-1] +'_4' + '.png')
    img5.save(files + '/'+ files[-1] +'_5' + '.png')
    img6.save(files + '/'+ files[-1] +'_6' + '.png')
    return files

# 图像转 32x32 txt格式
def Image2Txt(filename):
    if not os.path.exists(TO_DIR):
        os.mkdir(TO_DIR)
    im = Image.open(filename)
    im = im.convert('RGB')
    im = im.resize((32, 32), Image.ANTIALIAS)
    im.save(filename)
    txtName = TO_DIR + filename.split('.')[0].split('/')[-1] + '.txt'
    fh = open(txtName, 'a')
    width = im.size[0]
    height = im.size[1]
    for i in range(0, height):
        for j in range(0, width):
            cl = im.getpixel((j,i))
            clall = cl[0] + cl[1] + cl[2]
            if(clall) == 0:
                fh.write('1')
            else:
                fh.write('0')
        fh.write('\n')
    fh.close()
    return txtName

# 去除多余的空白
def ClearMore(filename):
    im = Image.open(filename)
    im = im.convert('RGB')
    width = im.size[0]
    height = im.size[1]
    flag = 0
    for i in range(0, height):
        for j in range(0, width):
            cl = im.getpixel((j, i))
            clall = cl[0] + cl[1] + cl[2]
            if clall != 255+255+255 and flag == 0:
                upper = i
                flag = 1

    flag = 0
    for i in range(0, width):
        for j in range(0, height):
            cl = im.getpixel((i, j))
            clall = cl[0] + cl[1] + cl[2]
            if clall != 255+255+255 and flag == 0:
                left = i
                flag = 1

    for i in range(0, height):
        for j in range(0, width):
            cl = im.getpixel((j, i))
            clall = cl[0] + cl[1] + cl[2]
            if clall != 255+255+255:
                lower = i

    for i in range(0, width):
        for j in range(0, height):
            cl = im.getpixel((i, j))
            clall = cl[0] + cl[1] + cl[2]
            if clall != 255+255+255:
                right = i

    im_new = im.crop((left, upper, right, lower))
    im_new.save(filename)

# 判断分数是几位数
def JugeTwo(filename):
    im = Image.open(filename)
    im = im.convert('RGB')
    width = im.size[0]
    height = im.size[1]
    flag = False
    tag = 0
    dit = 0
    for i in range(0, width):
        for j in range(0, height):
            cl = im.getpixel((i, j))
            clall = cl[0] + cl[1] + cl[2]
            if clall != 255 + 255 + 255 and tag == 0:
                dit = i
                tag = 1
    zero = dit

    for i in range(dit, width):
        sum = height * 3 * 255
        for j in range(0, height):
            cl = im.getpixel((i, j))
            clall = cl[0] + cl[1] + cl[2]
            sum -= clall
        if sum == 0 and tag == 1:
            dit = i
            tag = -(tag)
    one = dit

    for i in range(dit, width):
        for j in range(0, height):
            cl = im.getpixel((i, j))
            clall = cl[0] + cl[1] + cl[2]
            if clall != 255 + 255 + 255 and tag == -1:
                dit = i
                tag = (-(tag))+1
                flag = True
    two = dit
    return flag, zero, one, two

# 图片降噪
def clearNoise(image, N, Z):
    t2val = {}

    def twoValue(image, G):
        for y in range(0, image.size[1]):
            for x in range(0, image.size[0]):
                g = image.getpixel((x, y))
                if g > G:
                    t2val[(x, y)] = 1
                else:
                    t2val[(x, y)] = 0
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1

# 如果分数是两位数，则分成两个部分识别
def ClearTwo(filename, zero, one, two):
    im = Image.open(filename)
    width = im.size[0]
    height = im.size[1]
    im1 = im.crop((zero, 0, one, height))
    im2 = im.crop((two, 0 , width, height))
    filename1 = filename[:-4] + '_1' + filename[-4:]
    filename2 = filename[:-4] + '_2' + filename[-4:]
    im1.save(filename1)
    im2.save(filename2)
    return im1, im2, filename1, filename2

# 主要处理函数
def ProcessPicture():
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    fileList = listdir(BASE_DIR)
    List = []
    for i in fileList:
        g_path = locate(BASE_DIR + i)
        imgList = listdir(g_path)
        List_s = []
        for img in imgList:
            path = g_path + '/' + img
            toBlack(path)
            result = JugeTwo(path)
            if result[0] == False:
                ClearMore(path)
                txtName = Image2Txt(path)
                result = knn.handwriting(txtName)
                List_s.append(int(result))
            else:
                zero, one, two = result[1], result[2], result[3]
                im1, im2, filename1, filename2 = ClearTwo(path, zero, one, two)
                ClearMore(filename1)
                txtName1 = Image2Txt(filename1)
                result1 = knn.handwriting(txtName1)
                ClearMore(filename2)
                txtName2 = Image2Txt(filename2)
                result2 = knn.handwriting(txtName2)
                List_s.append(int(str(result1) + str(result2)))
        List.append(List_s)
        # List = kmeans.liss()
    # shutil.rmtree(BASE_DIR)
    # for i in listdir(TO_DIR):
    #     os.remove(TO_DIR + i)
    return List

if __name__ == '__main__':
    # 测试
    Image2Txt("C:/Users/Administrator/Desktop/333.jpg")
