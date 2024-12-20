#-*- coding: utf-8 -*-
#菜品盈利数据 帕累托图
import pandas as pd

#初始化参数
dish_profit = './catering_dish_profit.xls' #餐饮菜品盈利数据
data = pd.read_excel(dish_profit, index_col = u'菜品名')
data = data[u'盈利'].copy()
data.sort_values(ascending=False, inplace=True)

import matplotlib.pyplot as plt #导入图像库
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

#查看数据频数
# plt.figure(figsize=(12,8))
# data.plot(kind = 'bar', color = 'g', alpha = 0.8, width = 0.6,rot=0)

plt.figure()
data.plot(kind='bar')
plt.ylabel(u'盈利（元）')
p = 1.0*data.cumsum()/data.sum()

# 获取超过 70% 占比的节点值索引和索引位置
key = p[p > 0.7].index[0]
key_num = data.index.tolist().index(key)
print('超过70%占比的节点值索引为：', key)
print('超过70%占比的节点值索引位置为：', key_num)


p.plot(color='r', secondary_y=True, style='-o', linewidth=2)
plt.annotate(format(p.iloc[key_num], '.4%'), xy=(key_num, p.iloc[key_num]),
             xytext=(key_num * 0.9, p.iloc[key_num] * 0.9),
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
plt.ylabel(u'盈利（比例）')
plt.show()
