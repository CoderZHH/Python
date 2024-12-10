from __future__ import print_function
import pandas as pd
from apriori import *  # 导入自行编写的apriori函数

# 读取数据
user_goods = pd.read_excel('../data/goods.xls', header = None)
print(type(user_goods))
print(user_goods)

print('\n转换原始数据至0-1矩阵')
ct = lambda x : pd.Series(1, index = x[pd.notnull(x)])  # 转换0-1矩阵的过渡函数
b = map(ct, user_goods.values)  # 用map方式执行
data = pd.DataFrame(list(b)).fillna(0)  # 实现矩阵转换，空值用0填充
print('\n转换完毕')
del b  # 删除中间变量b，节省内存

support = 0.2  # 最小支持度
confidence = 0.5  # 最小置信度
ms = '---'  # 连接符，用来区分不同元素

# 关联规则分析并写出结果
apriori_result = find_rule(data, support, confidence, ms)
apriori_result = apriori_result.round(3)
apriori_result.to_excel('./apriori_result.xlsx')


