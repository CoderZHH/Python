import pandas as pd
# 读取训练样本和测试样本
data_train = pd.read_csv('../data/train.csv')
data_test = pd.read_csv('../data/test.csv')

# 对数据进行描述性统计分析
# 返回缺失值个数、最大值、最小值
# 训练样本的描述性统计分析
# 在describe函数中，percentiles参数表示指定计算的分位数表，如1/4分位数、中位数等
explore_train = data_train.describe(percentiles=[], include='all').T
explore_train['null'] = data_train.isnull().sum()  # 计算缺失值
explore_train = explore_train[['null', 'max', 'min']]
explore_train.columns = ['空值数', '最大值', '最小值']  # 表头重命名

# 测试样本的描述性统计分析
explore_test = data_test.describe(percentiles=[], include='all').T
explore_test['null'] = data_test.isnull().sum()  # 统计缺失值
explore_test = explore_test[['null', 'max', 'min']]
explore_test.columns = ['空值数', '最大值', '最小值']  # 表头重命名

# 写出结果
explore_train.to_csv('../tmp/explore_train.csv')  # 训练样本的描述性统计分析
explore_test.to_csv('../tmp/explore_test.csv')  # 测试样本的描述性统计分析

# 合并训练数据和测试数据
data1 = pd.concat([data_train, data_test], axis=0)
# 处理data_received属性、date属性
data1['date_received'] = data1['date_received'].astype('str').apply(
    lambda x: x.split('.')[0])
data1['date_received'] = pd.to_datetime(data1['date_received'])
data1['date'] = data1[ 'date'].astype('str').apply(lambda x: x.split('.')[0])
data1['date'] = pd.to_datetime(data1['date'])

# 绘制图形分析满减优惠和形式和折扣率优惠形式
import matplotlib.pyplot as plt
import re
indexOne = data1['discount_rate'].astype(str).apply(lambda x: re.findall(
    '\d+:\d+', x) != [])  # 满减优惠形式的索引
indexTwo = data1['discount_rate'].astype(str).apply(lambda x: re.findall(
    '\d+\.\d+', x) != [])  # 折扣率优惠形式的索引
dfOne = data1.loc[indexOne, :]  # 取出满减优惠形式的数据
dfTwo = data1.loc[indexTwo, :]  # 取出折扣率优惠形式的数据
# 在满减优惠形式的数据中，15天内优惠券被使用的数目
numberOne = sum((dfOne['date'] - dfOne['date_received']).dt.days <= 15)
# 在满减优惠形式的数据中，15天内优惠券未被使用的数目
numberTwo = len(dfOne) - numberOne
# 在折扣率优惠形式的数据中，15天内优惠券被使用的数目
numberThree = sum((dfTwo['date'] - dfTwo['date_received']).dt.days <= 15)
# 在折扣率优惠形式的数据中，15天内优惠券未被使用的数目
numberFour = len(dfTwo) - numberThree
# 绘制图形
plt.figure(figsize=(6, 3))
plt.rcParams['font.sans-serif'] = 'Simhei'
plt.subplot(1, 2, 1)
plt.pie([numberOne, numberTwo], autopct='%.1f%%', pctdistance=1.4)
plt.legend(['优惠券15天内被使用', '优惠券15天内未被使用'], fontsize=7, loc=(0.15, 0.91))  # 添加图例
plt.title('满减优惠形式', fontsize=15, y=1.05)  # 添加标题
plt.subplot(1, 2, 2)
plt.pie([numberThree, numberFour], autopct='%.1f%%', pctdistance=1.4)
plt.legend(['优惠券15天内被使用', '优惠券15天内未被使用'], fontsize=7, loc=(0.15, 0.91))  # 添加图例
plt.title('折扣率优惠形式', fontsize=15, y=1.05)  # 添加标题
plt.show()


# 提取月份
data_month = data1['date'].apply(lambda x: x.month) 

# 对各月份用户消费次数进行统计
data_count = data_month.value_counts().sort_index(ascending=True)

# 绘制用户消费次数折线图
fig = plt.figure(figsize=(8, 5))  # 设置画布大小
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', size=12)
plt.plot(data_count.index, data_count, color='#0504aa',
         linewidth=3.0, linestyle='-.')
plt.xlabel('月份')
plt.ylabel('消费次数')
plt.title('2016年各月用户消费次数')
plt.show()


# 提取领券日期的月份
received_month = data1['date_received'].apply(lambda x: x.month)
month_count = received_month.value_counts().sort_index(ascending=True)

# 获取领券消费数据
cop_distance = data1.loc[data1['date'].notnull()&data1[
    'coupon_id'].notnull(),['user_id', 'distance', 'date', 'discount_rate']]
# 统计领券消费次数
date_month = cop_distance['date'].apply(lambda x: x.month)
datemonth_count = date_month.value_counts().sort_index(ascending=True)
datemonth_countlist = list(datemonth_count)  # 转为列表

# 绘制用户领券次数与领券消费次数的柱形图
import numpy as np
fig = plt.figure(figsize=(8, 5))  # 设置画布大小
name_list = [i for i in range(1, 7)]; x = [i for i in range(1, 7)]
width = 0.4  # width设置宽度大小
plt.bar(x, height=list(month_count),
        width=width, label='用户领券', alpha=1, color='#0504aa')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, height=np.array(datemonth_countlist),
        width=width, label='用户领券消费', alpha=0.4, color='red')
plt.legend() # 图例
plt.xlabel('月份')
plt.ylabel('次数')
plt.title('2016年各月用户领券次数与领券消费次数')
plt.show()


# 提取商户投放优惠券数据 
coupon_data = data1.loc[data1['coupon_id'].notnull(), ['merchant_id', 'coupon_id']]
merchant_count = coupon_data['merchant_id'].value_counts()
print('参与投放优惠券商户总数为：', merchant_count.shape[0])
print('商户最多投放优惠券{max_count}张\n商户最少投放优惠券{min_count}张'.
      format(max_count=merchant_count.max(), min_count=merchant_count.min()))

# 绘制柱形图分析商家投放数量
fig = plt.figure(figsize=(8, 5))  # 设置画布大小
plt.rc('font', size=12)
plt.bar(x=range(len(merchant_count[:10])),
        height=merchant_count[:10], width=0.5,
        alpha=0.8, color='#0504aa')
# 给柱形图添加数据标注
for x, y in enumerate(merchant_count[:10]):
    plt.text(x-0.4, y+500, "%s" %y)
plt.xticks(range(len(merchant_count[:10])), merchant_count[:10].index)
plt.xlabel('商户ID')
plt.ylabel('投放优惠券数量')
plt.title('投放优惠券数量前10名的商户ID')
plt.show()


# 提取用户消费次数数据
date_distance = data1.loc[data1['date'].notnull() & data1[
        'distance'].notnull(), ['user_id', 'distance', 'date']]
print('数据形状:', date_distance.shape)

# 统计用户消费次数
dis_count = date_distance['distance'].value_counts()

# 绘制用户到门店消费的距离比例饼图
fig = plt.figure(figsize=(10, 10))  # 设置画布大小
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', size=15)
plt.pie(x=dis_count, labels=dis_count.index, labeldistance=1.2,
        pctdistance=1.4, autopct='%1.1f%%')

plt.title('用户到门店消费的距离比例', fontdict={'weight': 'normal','size': 25})
plt.show()


# 提取用户领券到店铺消费距离数据
cop_distance = data1.loc[data1['date'].notnull() & data1[
        'distance'].notnull()&data1['coupon_id'].notnull(), [
                'user_id', 'distance', 'date', 'discount_rate']]
print('数据形状:', cop_distance.shape) 
cop_count = cop_distance['distance'].value_counts()

# 提取用户未用券到店铺消费距离数据
nocop_distance = data1.loc[data1['date'].notnull() & data1[
        'distance'].notnull()&data1['coupon_id'].isnull(), [
                'user_id', 'distance', 'date', 'discount_rate']]
print('数据形状:', nocop_distance.shape)
nocop_count = nocop_distance['distance'].value_counts()

# 绘制用户持券到门店消费的距离比例饼图比例饼图
plt.figure(figsize=(12, 6))  # 设置画布大小
plt.subplot(1, 2, 1)  # 子图
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
plt.rcParams['axes.unicode_minus'] = False
plt.pie(x=cop_count, labels=cop_count.index, pctdistance=1.45,
        labeldistance=1.3, textprops=dict(fontsize=8), autopct='%1.1f%%')
plt.title('用户持券到门店消费的距离比例', fontdict={'weight': 'normal','size': 17})

# 绘制用户未持券直接到门店消费的距离比例饼图
plt.subplot(1, 2, 2)
plt.pie(x=nocop_count, labels=nocop_count.index, pctdistance=1.45,
        textprops=dict(fontsize=8), autopct='%1.1f%%')
plt.title('用户没用券直接到门店消费的距离比例', fontdict={'weight':'normal','size': 17})
plt.show()

