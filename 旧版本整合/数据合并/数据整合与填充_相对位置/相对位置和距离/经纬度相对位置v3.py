# -*- coding: utf-8 -*-
# 日期: 2019/5/31 23:02
# 作者: xcl
# 工具：PyCharm

# 相关库
from math import radians, cos, sin, asin, sqrt
from darksky import forecast  # DarkSkyAPI
import time  # 年度时间范围生成
from datetime import datetime as dt  # 时间戳日期转换
import pandas as pd  # BDS

import numpy as np
# import datetime
import math
import os

# 文件格式设置
pd.set_option('display.width', 6666)  # 设置字符显示宽度
pd.set_option('display.max_rows', None)  # 设置显示最大行
pd.set_option('display.max_columns', None)  # 设置显示最大列，None为显示所有列

# 参数设置
distance1 = 50000
distance2 = 100000

# 读取文件
coordinate_file_path = "F:\\毕业论文程序\\MODIS\\坐标\\"
JCZ_file = pd.read_excel(coordinate_file_path + "监测站坐标toDarkSkyAPI.xlsx", sheet_name="汇总")  # 监测站坐标toDarkSkyAPI

# 输出位置,待设置
out_path = ""
# 创建新数据框
coordinates = pd.DataFrame()
coordinates["xs"] = JCZ_file["经度"]
coordinates["ys"] = JCZ_file["纬度"]
coordinates["names"] = JCZ_file["城市"] + "-" + JCZ_file["监测点名称"]
# print(coordinates)

'''
# 距离
def geo_distance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    d_lon = lng2 - lng1
    d_lat = lat2 - lat1
    a = sin(d_lat/2)**2 + cos(lat1) * cos(lat2) * sin(d_lon/2)**2
    dis = 2*asin(sqrt(a))*6371.393*1000  # 地球半径
    return dis  # 输出结果的单位为“米”


# 尝试计算

# 方案1
for row1 in range(len(coordinates)):
    # print(coordinates[row1:row1+1])  # 万寿西宫到菏泽学院 每一个
    data1 = coordinates[row1:row1+1]  # 某一行
    data2 = coordinates.drop([row1])  # 删除行的数据
    # print(data1, data2, sep="\n")
    for row2 in range(len(data2)):
        data3 = data2[row2:row2+1]  # 某一行
        data4 = geo_distance(data1["xs"], data1["ys"], data3["xs"], data3["ys"])
        print(data4)
    print("\n")  # 断行


# 方案2
data5 = []
for row1 in range(len(coordinates)):
    # print(coordinates[row1:row1+1])  # 万寿西宫到菏泽学院 每一个
    data1 = coordinates[row1:row1+1]  # 某一行
    # print(data1, data2, sep="\n")
    data4 = []
    for row2 in range(len(coordinates)):
        data2 = coordinates[row2:row2+1]  # 某一行
        data3 = geo_distance(data1["xs"], data1["ys"], data2["xs"], data2["ys"])
        if data3 > distance2:
            data3 = "C"
        elif data3 >distance1 and data3 <= distance2:
            data3 = "B"
        else:
            data3 = "A"
        data4.append(data3)
    #  print(len(data4))
    #  print(data4)
    data5.append(data4)


data5 = pd.DataFrame(data5)
# print(data5)

# 修改行名称,索引
data5["name"] = coordinates["names"]
data6 = data5.set_index('name')

# 修改列
names = []
for name in data5["name"]:
    names.append(name)
data6.columns = names

print(data6)

data6.to_excel('data6.xlsx')


# -------------------------- 到此,已经完成了关于【距离】的交叉表格----------------------------
# 下一步 可以在计算距离时，把大于某范围的值直接删除或等于0等 ，避免再次遍历。
# 相对位置


# 方案1
data7 = []
for row1 in range(len(coordinates)):
    # print(coordinates[row1:row1+1])  # 万寿西宫到菏泽学院 每一个
    data1 = coordinates[row1:row1+1]  # 某一行
    # print(data1, data2, sep="\n")
    data4 = []
    for row2 in range(len(coordinates)):
        data2 = coordinates[row2:row2+1]  # 某一行
        # data3 = geo_distance(data1["xs"], data1["ys"], data2["xs"], data2["ys"])
        data3_x = float(data2["xs"]-data1["xs"].values)
        data3_y = float(data2["ys"]-data1["ys"].values)
        print(data3_x.__class__, data3_x)
        if data3_x == 0 and data3_y == 0:
            data3 = "self"  # 0
        elif data3_y != 0 and data3_x == 0:
            if data3_y > 0:
                data3 = "1"  # 1
            else:
                data3 = "5"  # 5
        elif data3_y == 0 and data3_x != 0:
            if data3_x > 0:
                data3 = "3"  # 3
            else:
                data3 = "7"  # 7
        elif data3_x > 0:
            data_k = data3_y/data3_x
            if data_k > 1:
                data3 = "1"  # 1
            elif data_k > 0 and data_k <= 1:
                data3 = "2"  # 2
            elif data_k <0 and data_k > -1:
                data3 = "3"  # 3
            elif data_k < -1:
                data3 = "4"  # 4
        elif data3_x < 0 :
            data_k = data3_y/data3_x
            if data_k > 1:
                data3 = "5"  # 5
            elif data_k > 0 and data_k <= 1:
                data3 = "6"  #  6
            elif data_k <0 and data_k > -1:
                data3 = "7"  # 7
            elif data_k < -1:
                data3 = "8"  # 8
        else:
            data3 = "bug"
        # data3 = str(data3)
        data4.append(data3)
    #  print(len(data4))
    #  print(data4)

    data7.append(data4)
data7 = pd.DataFrame(data7)

# 修改行名称,索引
data7["name"] = coordinates["names"]
data8 = data7.set_index('name')

# 修改列
names = []
for name in data7["name"]:
    names.append(name)
data8.columns = names

print(data8)

data8.to_excel('data8-2.xlsx')


# -------------------------- 到此,已经完成了关于【相对位置】的交叉表格----------------------------
# 表格结果为 列标题在行标题的第*分类上


# 下一步结合距离

table1 = pd.read_excel("data6.xlsx")
table2 = pd.read_excel("data8-2.xlsx")

table3 = pd.DataFrame()
for namess in table2.columns:
    # table3[namess] = table2[namess] + "-" + table1[namess]
    table3[namess] = table1[namess] + "-" + table2[namess]

table3['name'] = coordinates["names"]
table3 = table3.set_index('name')
table3.to_excel("table3.xlsx")
'''
# -------------------------- 到此,已经完成了关于【相对位置+距离】的交叉表格----------------------------
# 表格结果为 列标题在行标题的第*分类上

data_location = pd.read_excel("table3.xlsx")
# print(data_location.head())
data_aod = "F:\\毕业论文程序\\气溶胶光学厚度\\日均\\"
for location in data_location["name"]:
    #print(data_location[data_location["name"] == location])  # 按行输出
    data_aod_outcome = pd.read_excel(data_aod + location + ".xlsx")
    data_aod_outcome = data_aod_outcome.set_index('日期')
    data_need_to_extract = data_location[data_location["name"] == location]
    same_area = []
    for element in data_need_to_extract.columns:
        value_1 = data_need_to_extract[element].values  # 每个单元格的值
        #print(value_1)

        if value_1 == "A-1":  # 第一个区划
            #print(value_1)
            same_area.append(element)

    print(same_area)
    if len(same_area) != 0:
        xi = 0
        for area in same_area:
            xi = xi + 1
            #print(area)
            data_to_merge = pd.read_excel(data_aod + area + ".xlsx")
            data_to_merge = data_to_merge.set_index('日期')
            # print(data_to_merge.head())
            # 尝试把列名改成A-4-xxx 多一个 - 方便 删除
            data_to_merge.rename(columns={'监测站': 'A-1-监测站-%s' % xi, 'AOD值': 'A-1-AOD值-%s' % xi}, inplace=True)
            #print(data_to_merge.head())
            data_aod_outcome = pd.concat([data_aod_outcome, data_to_merge], axis=1, join_axes=[data_aod_outcome.index])
            data_aod_outcome['A-1-AOD值-%s' % xi] = data_aod_outcome['A-1-AOD值-%s' % xi].fillna(0)
    else:
        print("无临近监测站")
    if xi != 0:
        for xj in range(1, xi+1):
            print(xj)

    item_add = []
    for item in data_aod_outcome.columns:

        if "A-1-AOD值" in item:
            item_add.append(item)
            #print(item)
        else:
            pass
            #print("none")
    #print(item_add)
            # data_aod_outcome["A1-mean"] = (data_aod_outcome["A-1-AOD值-%s"] + data_aod_outcome["A-1-AOD值-%s"])/xi
            #locals()['df' + str(xj)] = data_aod_outcome["A-1-AOD值-%s" % xj]
    if len(item_add) != 0:
        data_aod_outcome["A1-AOD-MEAN"] = data_aod_outcome[item_add].mean(axis=1)  # 均值换轴
    print(data_aod_outcome[item_add])

    #print(data_aod_outcome.head())


    data_aod_outcome.to_excel("F:\\毕业论文程序\\整合数据\\整合1\\%s.xlsx" % location)

