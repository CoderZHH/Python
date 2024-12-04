# 绘制不同部门的各月份销售额折线图
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_excel('./各月份各部门销售额.xlsx')
plt.figure(figsize=(6, 4))

plt.plot(data['月份'], data['销售部'], color='green', label='销售部', marker='o')
plt.plot(data['月份'], data['事业部'], color='red', label='事业部', marker='s')
#plt.plot(data['月份'], data['行政部'], color='skyblue', label='行政部', marker='x')
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.legend()  # 显示图例
plt.title('各部门各月份销售额')
plt.ylabel('销售额（万元）')
plt.xlabel('月份')
plt.savefig('../1.jpg', dpi=1080, bbox_inches='tight')
plt.show()

# 绘制销售部各年份各月份的销售额折线图
data = pd.read_excel('./销售部在各年份各月份中的销售额.xlsx')
plt.figure(figsize=(6, 4))
plt.plot(data['月份'], data['2017年'], color='green', label='2017年', marker='o')
plt.plot(data['月份'], data['2018年'], color='red', label='2018年', marker='s')
plt.plot(data['月份'], data['2019年'], color='skyblue', label='2019年', marker='x')
plt.legend()  # 显示图例
plt.title('销售部各年份各月份销售额')
plt.ylabel('销售额（万元）')
plt.xlabel('月份')
plt.savefig('../2.jpg', dpi=1080, bbox_inches='tight')
plt.show()
