# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/8/30 19:52

"""
更新 try,except
修复迭代法的bug
"""

# 库
from multiprocessing import Process  # 多线程,提高CPU利用率
import copy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
from fancyimpute import IterativeImputer  # 方法创建新的数据框,不覆盖原始数据
import os

# 路径
input_file_path_darksky_weather = "D:\\毕业论文程序\\气象数据\\筛除字符串\\2018_日期补全\\"
JCZ_info = pd.read_excel(
    "D:\\毕业论文程序\\MODIS\\坐标\\监测站坐标.xlsx",
    sheet_name="汇总")  # 152个
JCZ_info["监测站"] = JCZ_info["城市"] + "-" + JCZ_info["监测点名称"]
# 已经输出


def get4method(xx152):
    # 地理距离
    def geo_distance(lng1_df, lat1_df, lng2_df, lat2_df):
        lng1_df, lat1_df, lng2_df, lat2_df = map(
            radians, [lng1_df, lat1_df, lng2_df, lat2_df])
        d_lon = lng2_df - lng1_df
        d_lat = lat2_df - lat1_df
        a = sin(d_lat / 2) ** 2 + cos(lat1_df) * \
            cos(lat2_df) * sin(d_lon / 2) ** 2
        dis = 2 * asin(sqrt(a)) * 6371.393 * 1000  # 地球半径
        return dis  # 输出结果的单位为“米”

    # 监测站
    jcz_152 = pd.read_excel(
        "D:\\毕业论文程序\\MODIS\\坐标\\站点列表-2018.11.08起_152.xlsx",
        sheet_name=xx152)
    jcz_152["监测站名称_152"] = jcz_152["城市"] + "-" + jcz_152["监测点名称"]
    for input_file_name in jcz_152["监测站名称_152"]:
        input_file_name = input_file_name + ".xlsx"
        # if input_file_name in saved_list:
        # print("已经完成:", input_file_name, xx152)
        # continue
        print("========正在计算%s========" % input_file_name)
        try:
            # 读取数据源
            data_darksky_weather = pd.read_excel(
                input_file_path_darksky_weather + input_file_name)
            data_darksky_weather = data_darksky_weather.set_index('日期')
            # 空间
            name = str(input_file_name).replace(".xlsx", "")  # 定义相关变量
            lng1 = JCZ_info[JCZ_info["监测站"] == name]["经度"]
            lat1 = JCZ_info[JCZ_info["监测站"] == name]["纬度"]
            # 空间全局: 迭代回归,缺失特征作为y,其他特征作为x
            merge_list = []  # 同一监测站,不同污染物
            for darksky_weather_Iterative in [
                'apparentTemperatureHigh',
                'apparentTemperatureLow',
                'apparentTemperatureMax',
                'apparentTemperatureMin',
                'cloudCover',
                'dewPoint',
                'humidity',
                'moonPhase',
                'ozone',
                'precipAccumulation',
                'precipIntensity',
                'precipIntensityMax',
                'pressure',
                'sunriseTime',
                'sunsetTime',
                'temperatureHigh',
                'temperatureLow',
                'temperatureMax',
                'temperatureMin',
                'uvIndex',
                'visibility',
                'windBearing',
                'windGust',
                'windSpeed',
                'apparentTemperature',
                    'temperature']:
                concat_list = []  # 用于添加同污染物,不同监测站的数值
                numb = 0
                for item in JCZ_info["监测站"]:  # 不同于气溶胶插值方法
                    if item != name:
                        lng_2 = JCZ_info[JCZ_info["监测站"] == item]["经度"]
                        lat_2 = JCZ_info[JCZ_info["监测站"] == item]["纬度"]
                        dis_2 = geo_distance(
                            lng1, lat1, lng_2, lat_2)  # 两站地理距离
                        if dis_2 > 0:  # 合并所有152个
                            data_to_add_in_to_Iterative = pd.read_excel(
                                input_file_path_darksky_weather + item + ".xlsx")
                            data_to_add_in_to_Iterative = data_to_add_in_to_Iterative.set_index(
                                "日期")
                            # 列名
                            data_to_Iterative_concat = data_to_add_in_to_Iterative[
                                darksky_weather_Iterative]
                            data_to_Iterative_concat = pd.DataFrame(
                                data_to_Iterative_concat)
                            data_to_Iterative_concat.columns = [
                                darksky_weather_Iterative + "_add%s" %
                                numb]  # 如果有五个临近, 则NDVI1-NDVI5
                            concat_list.append(data_to_Iterative_concat)
                            numb += 1
                if len(concat_list) > 0:  # 合并本身与临近
                    data_to_Iterative = pd.concat(
                        concat_list, axis=1, sort=False)
                    data_to_Iterative = pd.concat(
                        [data_darksky_weather[darksky_weather_Iterative], data_to_Iterative], axis=1, sort=False)
                else:
                    data_to_Iterative = data_darksky_weather[darksky_weather_Iterative].copy(
                    )
                    data_to_Iterative = pd.DataFrame(data_to_Iterative)
                    data_to_Iterative.columns = [
                        darksky_weather_Iterative]  # 本身
                count_1 = 0
                for value_1 in data_to_Iterative.sum():
                    if value_1 != 0:
                        count_1 += 1
                if count_1 > 1:  # 至少两个非空列才可以计算
                    data_darksky_weather_Iterative_to_merge = IterativeImputer(
                        max_iter=10).fit_transform(data_to_Iterative)
                else:
                    data_darksky_weather_Iterative_to_merge = copy.deepcopy(
                        data_to_Iterative)
                data_darksky_weather_Iterative_to_merge = pd.DataFrame(
                    data_darksky_weather_Iterative_to_merge)  # 格式转换
                data_darksky_weather_Iterative_to_merge = data_darksky_weather_Iterative_to_merge.set_index(
                    data_to_Iterative.index)  # ok
                if len(
                        data_darksky_weather_Iterative_to_merge.columns) < len(
                        data_to_Iterative.columns):
                    reset_col_name_list = []  # 对非nan列先命名
                    for col_name in data_to_Iterative:
                        if np.max(data_to_Iterative[col_name]) > 0:
                            reset_col_name_list.append(col_name)
                    data_darksky_weather_Iterative_to_merge.columns = reset_col_name_list

                    for col_name in data_to_Iterative:  # 对缺失的nan列补充
                        if col_name not in data_darksky_weather_Iterative_to_merge:
                            # 补全缺失nan列
                            data_darksky_weather_Iterative_to_merge[col_name] = np.nan
                else:
                    data_darksky_weather_Iterative_to_merge.columns = data_to_Iterative.columns  # 重设列名
                for numb_del in range(numb):
                    del data_darksky_weather_Iterative_to_merge[darksky_weather_Iterative +
                                                                "_add%s" %
                                                                numb_del]
                merge_list.append(data_darksky_weather_Iterative_to_merge)  # 插补后的该监测点的气象特征列, 仅一列, 循环添加其他特征
            data_darksky_weather_Iterative = pd.concat(
                merge_list, axis=1, sort=False)

            # 对结果的0值取np.nan
            data_darksky_weather_Iterative.replace(0, np.nan, inplace=True)

            # 合并相同方法的结果
            data_darksky_weather_Iterative = data_darksky_weather_Iterative.set_index(
                data_darksky_weather.index)
            data_darksky_weather_Iterative.columns = data_darksky_weather.columns

            # 文件
            data_darksky_weather_Iterative.to_excel('D:\\气象迭代2018\\'+input_file_name)
        except Exception as e:
            print(input_file_name, "发生错误:", e)


if __name__ == '__main__':
    print('=====主进程=====')

    p1 = Process(target=get4method, args=("V4P1",))
    p2 = Process(target=get4method, args=('V4P2',))
    p3 = Process(target=get4method, args=('V4P3',))    # 样例3ok
    p4 = Process(target=get4method, args=('V4P4',))
    p5 = Process(target=get4method, args=('V4P5',))  # 样例5ok
    p6 = Process(target=get4method, args=('V4P6',))  # 样例6ok

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    p6.join()  # 依次检测是否完成, 完成才会执行join下面的代码
    p5.join()
    p4.join()
    p3.join()
    p2.join()
    p1.join()

    # 自动关机
    print("程序已完成," + str(60) + '秒后将会关机')
    print('关机')
    os.system('shutdown -s -f -t 60')
