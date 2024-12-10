import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dish = pd.read_csv('./meal_dishes_detail.csv', encoding='utf-8')  # 读取菜品详情表
info = pd.read_csv('./meal_order_info.csv', encoding='utf-8')  # 读取订单表
detail = pd.read_csv('./meal_order_detail.csv', encoding='utf-8')  # 读取订单详情表

# 统计订单状态为0或2的订单占比
info_id = info[['info_id']][(info.order_status == 0) | (info.order_status == 2)]["info_id"].tolist()
proportion = len(info_id) / info.shape[0]

# 提取订单状态为1的数据
info_1 = info[info['order_status'] == 1]
print('info_11111111111111:', info_1)
info_1 = info_1.reset_index(drop=True)
info_1.to_csv('./info.csv', encoding='utf-8')

# 统计每日用餐人数与营业额
for i, k in enumerate(info_1['use_start_time']):
    y = k.split()
    y = pd.to_datetime(y[0])
    info_1.loc[i, 'use_start_time'] = y

print('info_1', info_1)
groupbyday = info_1[['use_start_time', 'number_consumers', 'accounts_payable']].groupby(by='use_start_time')
print('groupbyday:', groupbyday)
sale_day = groupbyday.sum()
print('sale_day:', sale_day)
sale_day.columns = ['人数', '销量']
sale_day.to_csv('./sale_day.csv', encoding="utf-8_sig")

# 每日用餐人数和营业额折线图
plt.figure(figsize=(10, 4))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, ax1 = plt.subplots()  # 使用subplots函数创建窗口
ax1.plot(sale_day['人数'], '--')
ax1.set_yticks(range(0, 900, 100))  # 设置y轴的刻度范围
ax1.legend(('用餐人数',), loc='upper left', fontsize=10)
ax2 = ax1.twinx()  # 创建第二个坐标轴
ax2.plot(sale_day['销量'])
ax2.legend(('营业额',), loc='upper right', fontsize=10)
ax1.set_xlabel('日期')
ax1.set_ylabel('用餐人数')
ax2.set_ylabel('营业额（元）')
plt.gcf().autofmt_xdate()  # 自动适应刻度线密度，包括x轴、y轴
plt.title('每日用餐人数和营业额')
plt.show()

# 删除detail数据中无意义的订单
nomean_index = detail[detail['order_id'].apply(lambda x: x in info_id)].index.tolist()
detail = detail.drop(nomean_index)

# 去掉订单详情表中菜品名称的换行符和回车符
detail['dishes_name'] = detail['dishes_name'].apply(lambda x: x.replace(' ', '').replace('\n', '').replace('\r', ''))

# 处理时间数据
detail['place_order_time'] = pd.to_datetime(detail['place_order_time'])
detail.to_csv('./detail.csv', encoding='utf-8')

# 提取place_order_time大于20160801且小于20180831的订单详情数据
detail_data = detail[(detail['place_order_time'] >= pd.to_datetime('20160801')) &
                     (detail['place_order_time'] <= pd.to_datetime('20180831'))]

# 分组聚合对counts计数并求出最大值和最小值
sales_volume = pd.DataFrame(detail_data.groupby(by=['dishes_name'])['counts'].count())
sales_volume['dishes_name'] = sales_volume.index.tolist()
sales_volume = sales_volume.reset_index(drop=True)
Qmax = np.max(sales_volume['counts'])
Qmin = np.min(sales_volume['counts'])

# 将'sales_hot'列显式转换为float类型
sales_volume['sales_hot'] = 0.0

# 利用for循环计算菜品热销度
for i in range(sales_volume.shape[0]):
    sales_volume.loc[i, 'sales_hot'] = round((sales_volume.loc[i, 'counts'] - Qmin) / (Qmax - Qmin), 2)

# 根据热销度进行降序排序，并写出数据
sales_volume = sales_volume.sort_values(by='sales_hot', ascending=False)
sales_volume.to_csv('./sales_volume.csv', encoding='utf-8_sig')

# 查看热销度前10的菜品信息
sales_volume.head(10)

# 绘制图形
plt.figure()
plt.bar(sales_volume.head(10)['dishes_name'], sales_volume.head(10)['counts'])
plt.title('热销度前10名的菜品')
plt.xlabel('菜品名称')
plt.ylabel('销售数量')
plt.xticks(rotation=60)
plt.show()
