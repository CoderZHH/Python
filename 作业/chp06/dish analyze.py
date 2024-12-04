#-*- coding: utf-8 -*-
import pandas as pd

#初始化参数
dish_profit = '../data/catering_sale.xls' #餐饮菜品盈利数据
data = pd.read_excel(dish_profit, index_col = u'日期')
#缺失值处理？


statistics = data.describe() #保存基本统计量
statistics.loc['range'] = statistics.loc['max']-statistics.loc['min'] #极差
print(statistics)

#分组
groupNum = 9084/500
print(groupNum)
#18
gNum = 18

#直方图
import matplotlib.pyplot as plt

plt.hist(data, bins=gNum, edgecolor='black')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Data')
plt.show()