# -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/20  23:52 
# -*- coding: utf-8 -*-
# 作者：xcl
# 时间：2019/6/20  21:27

from sklearn.ensemble import AdaBoostRegressor
from keras.models import Sequential, Model
from keras import layers, Input
import numpy as np
import pandas as pd
from keras.utils import to_categorical
from sklearn.utils import shuffle
from sklearn.model_selection import KFold,StratifiedKFold
import datetime  # 程序耗时

# 开始计算耗时
start_time = datetime.datetime.now()
# 读取
#data = pd.read_excel("相邻位置仅留PM和T-1.xlsx")
input_path = 'D:\\雨雪+2018_new_pm_aod_interpolate.xlsx'

data = pd.read_excel(input_path)
#data = pd.read_excel("测试用数据.xlsx")
# 设置变量
"""
data = data[data["AOD值"] > 0]
data["AOD值"] = data["AOD值"] / 1000
data = data[data["日均PM2.5"] > 0]
data = data[data["AOD值"] < 2001]
"""

independent = ["AOD_0", 'cloudCover', 'dewPoint', 'humidity', 'precipAccumulation', 'precipIntensity', 'pressure',
               'temperature', 'uvIndex', 'visibility', 'windSpeed', 'windBearing']
T_1 = ['AOD_0', 'pressure_T1']
PM_list = ['AOD_0']
dependent = ["PM25"]
# jcz = ["监测站"]
''''''
xni = pd.get_dummies(data['id'])


# independent = list(set(independent) | set(T_1))  # 合集
# 更改为数组格式与独热编码
'''
data_x1 = data[independent]
data_x2 = data[PM_list]
data_y = data[dependent]
data_x1 = np.array(data_x1)
data_x2 = np.array(data_x2)
data_y = np.array(data_y)
'''
# print(len(data_x1))


#  尝试独热编码
'''
data_x1 = to_categorical(data_x1)
data_x2 = to_categorical(data_x2)
data_y = to_categorical(data_y)
'''
###################################################################################

# 输入1和2的变量数,维度 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!是否可以不同维度
inputA = Input(shape=(12,))
inputB = Input(shape=(1,))
inputC = Input(shape=(2,))
inputD = Input(shape=(xni.shape[1],))
# 输入1
x = layers.Dense(24, activation="relu")(inputA)
x = layers.Dense(1, activation="relu")(x)
x = Model(inputs=inputA, outputs=x)
# 输入2
y = layers.Dense(32, activation="relu")(inputB)
y = layers.Dense(16, activation="relu")(y)
y = layers.Dense(1, activation="relu")(y)
y = Model(inputs=inputB, outputs=y)
# 输入3
x3 = layers.Dense(5, activation="relu")(inputC)
x3 = layers.Dense(1, activation="relu")(x3)
x3 = Model(inputs=inputC, outputs=x3)
# 输入4
x4 = layers.Dense(128, activation="relu")(inputD)
x4 = layers.Dense(64, activation="relu")(x4)
x4 = layers.Dense(16, activation="relu")(x4)
x4 = layers.Dense(1, activation="relu")(x4)
x4 = Model(inputs=inputD, outputs=x4)
# 合并多输入
combined = layers.concatenate([x.output, y.output, x3.output, x4.output])
# 输出层
z = layers.Dense(4, activation="relu")(combined)
z = layers.Dense(1, activation="sigmoid")(z)  ################ 最后的输出维度最好对应预测目标
############################################################# 建议最后用sigmoid
# 建立模型
model = Model(inputs=[x.input, y.input, x3.input, x4.input], outputs=z)
# 模型编译
model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])


print('#######打乱数据#######')
# 打乱
data = shuffle(data)  # , random_state=0
print("样本量:", len(data))

print('#######进行K折分组#######')
# k折分组,训练和测试 9:1
kf = KFold(n_splits=10)  # 参数shuffle=True

error_AME = []
error_MSE = []
error_RE = []
for train, test in kf.split(data):

    # 划分
    x1_train = data.iloc[train][independent]
    x1_test = data.iloc[test][independent]
    x2_train = data.iloc[train][PM_list]
    x2_test = data.iloc[test][PM_list]
    x3_train = data.iloc[train][T_1]
    x3_test = data.iloc[test][T_1]
    y_train = data.iloc[train][dependent]
    y_test = data.iloc[test][dependent]

    x4_train = xni.iloc[train]
    x4_test = xni.iloc[test]


    # np 格式

    x1_test_np = np.array(x1_test)
    x1_train_np = np.array(x1_train)
    x2_test_np = np.array(x2_test)
    x2_train_np = np.array(x2_train)
    x3_test_np = np.array(x3_test)
    x3_train_np = np.array(x3_train)
    y_test_np = np.array(y_test)
    y_train_np = np.array(y_train)

    x4_test_np = np.array(x4_test)
    x4_train_np = np.array(x4_train)
    # 模型计算
    '''
    ensemble = AdaBoostRegressor(base_estimator=model, learning_rate=0.001,
                                 loss='linear')
    ensemble.fit(X=[x1_train_np, x2_train_np], y=y_train_np)
    res = ensemble.predict([x1_test_np, x2_test_np])

    '''
    model.fit([x1_train_np, x2_train_np, x3_train_np, x4_train_np], y_train_np, epochs=1000, batch_size=256)
    res = model.predict([x1_test_np, x2_test_np, x3_test_np, x4_test_np])

    res = pd.DataFrame(res)
    y_test = pd.DataFrame(y_test)
    # 相同索引方便合并
    res.index = y_test.index
    data_pred = pd.concat([res, y_test], axis=1)
    data_pred.columns = ["pre", "true"]
    # 计算误差
    e_AME = abs(data_pred["pre"] - data_pred["true"]).mean()
    # print("AME误差:", e)
    e_MSE = ((data_pred["pre"] - data_pred["true"]) ** 2).mean()
    error_AME.append(e_AME)
    error_MSE.append(e_MSE)
    # 相对误差百分比
    r_e = (abs(data_pred["pre"] - data_pred["true"])/abs(data_pred["true"])).mean()
    #print(r_e, data_pred["true"])
    error_RE.append(r_e)
    #print(error_RE)
print("交叉验证后的平均AME误差值:", np.average(error_AME), "预测结果的标准差", np.std(error_AME))
print("交叉验证后的平均MSE误差值:", np.average(error_MSE), "预测结果的标准差", np.std(error_MSE))
print("相对误差:", np.average(error_RE),  "预测结果的标准差", np.std(error_RE))
end_time = datetime.datetime.now()
print(str(end_time - start_time))