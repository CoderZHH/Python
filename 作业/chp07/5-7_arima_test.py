# -*- coding: utf-8 -*-
# arima时序模型

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

# 参数初始化
discfile = 'arima_data.xlsx'
forecastnum = 5

# 读取数据，指定日期列为指标，Pandas自动将“日期”列识别为Datetime格式
data = pd.read_excel(discfile, index_col='日期')
data.index = pd.to_datetime(data.index)  # 确保索引为时间格式
data = data.asfreq('D')

# 时序图
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
data.plot()
plt.title("原始数据时序图")
plt.show()

# 自相关图
plot_acf(data).show()

# 平稳性检测
adf_result = ADF(data['销量'])
print('原始序列的ADF检验结果为：', adf_result)

# 差分后的结果
D_data = data.diff().dropna()
D_data.columns = ['销量差分']
D_data.plot(title="差分后时序图")  # 时序图
plt.show()

plot_acf(D_data).show()  # 自相关图
plot_pacf(D_data).show()  # 偏自相关图

adf_result_diff = ADF(D_data['销量差分'])
print('差分序列的ADF检验结果为：', adf_result_diff)

# 白噪声检验
ljung_box_result = acorr_ljungbox(D_data, lags=10)
print('差分序列的白噪声检验结果为：\n', ljung_box_result)

# 定阶
data['销量'] = data['销量'].astype(float)
pmax = int(len(D_data) / 10)  # 一般阶数不超过 length / 10
qmax = int(len(D_data) / 10)  # 一般阶数不超过 length / 10
bic_matrix = []  # bic 矩阵

for p in range(pmax + 1):
    tmp = []
    for q in range(qmax + 1):
        try:
            model = ARIMA(data, order=(p, 1, q)).fit()
            tmp.append(model.bic)
        except Exception as e:
            tmp.append(np.nan)  # 如果模型报错，则填充为 NaN
    bic_matrix.append(tmp)

bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值
print("BIC矩阵：\n", bic_matrix)

if bic_matrix.isnull().all().all():
    print("BIC矩阵为空，请检查数据或模型输入是否有问题！")
else:
    # 寻找 BIC 最小值对应的 p 和 q
    p, q = bic_matrix.stack().idxmin()
    print(f"BIC最小的p值和q值为：{p}、{q}")

    # 建立 ARIMA 模型
    model = ARIMA(data, order=(p, 1, q)).fit()
    print(model.summary())  # 输出模型报告

    # 预测未来 n 天
    forecast_result = model.forecast(forecastnum)
    print(f"未来 {forecastnum} 天的预测结果为：\n", forecast_result)
