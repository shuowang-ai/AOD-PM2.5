# -*- coding: utf-8 -*-
# 作者: xcl
# 时间: 2019/10/10 14:56


# 库
import pandas as pd
import numpy as np
import os
import random

list1 = []
list2 = []
list3 = []

for i in range(0,100):
    a = random.uniform(25, 32)
    b = random.uniform(0.65, 0.99)

    list1.append(a)
    list2.append(b)
    list3.append(a*a)

list4 = []
list4.append(list1)
list4.append(list2)
list4.append(list3)

df = pd.DataFrame(list4)
df.to_excel('test.xlsx')