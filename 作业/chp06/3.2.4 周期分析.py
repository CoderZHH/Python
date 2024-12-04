import pandas as pd
import matplotlib.pyplot as plt
# 绘制景区人流量趋势折线图
normal = pd.read_excel('../data/某观光景区3月份人流量.xlsx')
plt.figure(figsize=(8, 4))
plt.plot(normal['日期'], normal['人流量'])
plt.xlabel('日期')
x_major_locator = plt.MultipleLocator(7)  # 设置x轴刻度间隔
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.ylabel('人流量')
plt.title('景区人流量趋势')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于正常显示中文标签
plt.show()  # 展示图片
