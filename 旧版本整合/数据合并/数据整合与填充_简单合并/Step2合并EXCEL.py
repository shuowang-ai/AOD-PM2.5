# -*- coding: utf-8 -*-
# 日期: 2019/2/23 19:36
# 作者: xcl
# 工具：PyCharm

import pandas as pd
import os
# 参数设置
location = "-"
input_file_path = "F:\\毕业论文程序\\整合数据\\各监测站\\日均\\"  # HDF文件位置 TTT
output_file_path = "F:\\毕业论文程序\\整合数据\\各地区\\日均\\"  # 结果的输出位置

# 批量读取
file_name = os.listdir(input_file_path)  # 文件名

file_location_name = []
for name in file_name:
    if location in name:  # 通过文件名包含关键字的方法进行文件筛选
        file_location_name.append(name)
print(file_location_name, len(file_location_name), sep="\n")

list_file = []
for file in file_location_name:
    data = pd.read_excel(input_file_path+file)
    list_file.append(data)

df = pd.concat(list_file, sort=True, axis=0)

# print(df.isnull().sum())

# 删除值为空的数据
# df = df.dropna()
# print(df.isnull().sum())

# 删除全0列
# print(df.std())
df_std = pd.DataFrame(df.std())
list_0 = []
# print(df_sum.index)
# print(df_sum[0]["AOD值"])
'''
for key in df_std.index:
    if df_std[0]["%s" % key] == 0:
        print("删除", key)
        list_0.append(key)
df = df.drop(list_0, axis=1)
'''
# 索引
# 日均下 日期格式已经为dt.date
# df["日期"] = df["日期"].dt.date
df = df.set_index('日期')
# 导出
# df.to_csv(output_file_path+"%s.csv" % location)
df.to_excel(output_file_path+"%s.xlsx" % "总地区")
