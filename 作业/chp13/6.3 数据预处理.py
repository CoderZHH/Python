# 描述性统计分析
import pandas as pd

# 读取数据文件
credit = pd.read_csv('./credit_card.csv', encoding='GBK')
# 删除信用卡顾客编号属性
credit = credit.drop('信用卡顾客编号', axis=1)
length = len(credit)  # 计算数据量


# 定义描述性统计函数,且将结果保留3位小数
def status(x):
    return pd.Series([x.count(), length - x.count(), len(credit.groupby(by=x)), x.max() - x.min(),
                      x.quantile(.75) - x.quantile(.25), x.mode()[0], format(x.var(), '.3f'),
                      format(x.skew(), '.3f'), format(x.kurt(), '.3f')], index=['非空值数', '缺失值数',
                                                                                '类别数', '极差', '四分位差', '众数',
                                                                                '方差', '偏度', '峰度'])


# 应用描述性统计函数
describe_tb = credit.apply(status)
print(describe_tb)

import matplotlib.pyplot as plt
from collections import OrderedDict

plt.rcParams['font.family'] = 'SimHei'  # 正常显示中文

plt.figure(figsize=(5, 4))  # 设置画布大小
plt.bar(['是'], credit['瑕疵户'].value_counts()[1], color='r', width=0.3)
plt.bar(['否'], credit['瑕疵户'].value_counts()[2], color='b', width=0.3)
plt.ylabel('客户数量', fontsize=12)  # 设置y轴坐标和字体大小
plt.title('瑕疵户', fontsize=12)  # 设置标题和字体大小
plt.show()


# 编写瑕疵户与信用记录之间的关系函数
def credit_plot(column, i):
    ax = plt.subplot(3, 2, i)  # 子画布
    is_data = credit[credit['瑕疵户'] == 1][column]  # 瑕疵户数据
    not_data = credit[credit['瑕疵户'] == 2][column]  # 非瑕疵户数据
    is_y = is_data.value_counts() / is_data.shape[0]  # y数据
    ax.bar(1, is_y[1], color='r', label='是', width=0.3)  # 绘制柱状图
    if len(is_y) == 2:
        ax.bar(1, is_y[2], bottom=is_y[1], color='b', width=0.3)  # 柱堆叠
    not_y = not_data.value_counts() / not_data.shape[0]  # y数据
    ax.bar(2, not_y[1], color='r', width=0.3)  # 绘制柱形图
    ax.bar(2, not_y[2], bottom=not_y[1], color='b', label='否', width=0.3)  # 绘制柱形图
    ax.set_xticks([1, 2])  # 设置x轴坐标
    ax.set_xticklabels(['是', '否'], fontsize=14)  # 设置x轴坐标标签
    plt.ylabel('占比', fontsize=14)  # 设置y标题
    plt.title(column, fontsize=14)  # 设置标题
    plt.tight_layout()  # 调整子图间距


plt.figure(figsize=(9, 9))  # 设置画布大小

# 绘制瑕疵户与信用记录关系图
credit_plot('逾期', 1)
credit_plot('呆账', 2)
credit_plot('强制停卡记录', 3)
credit_plot('退票', 4)
credit_plot('拒往记录', 5)
plt.legend(loc=[2.3, 3.3], fontsize=12, handlelength=1)  # 添加图例
plt.show()


# 定义绘制客户经济情况分析直方图的函数
def economic_plot(column, tick, a):
    ax = plt.subplot(2, 2, a)  # 子图
    situ = sorted(credit[column].unique())  # 排序
    x = [i for i in range(len(situ))]  # x轴坐标数据
    y = [credit[column].value_counts()[i] for i in situ]  # y轴数据
    ax.bar(x, y, width=0.3)  # 绘制柱状图
    plt.ylabel('数量', fontsize=14)  # y轴坐标轴标题
    plt.xticks(rotation=30)  # x轴坐标轴标签倾斜程度
    ax.set_xticks([i for i in range(len(x))])  # 重设x轴坐标数据
    ax.set_xticklabels(tick, fontsize=14)  # 设置x轴显示坐标数据
    ax.set_xlabel(column + '（万元）', fontsize=14)  # y轴坐标轴标题
    plt.tight_layout()  # 控制子图之间的距离


plt.figure(figsize=(10, 8))

# 设置x轴坐标
tick1 = ['1以下', '1~2', '2~3', '3~4', '4以上']  # 个人月开销
tick2 = ['2以下', '2~4', '4~6', '6~8', '8~10', '10~15', '15~20', '20以上']  # 月刷卡额
tick3 = ['无收入', '0~1', '1~2', '2~3', '3~4', '4~5', '5~6', '6以上']  # 个人月收入
tick4 = ['未知', '2以下', '2~4', '4~6', '6~8', '8~10', '10以上']  # 家庭月收入
economic_plot('个人月开销', tick1, 1)
economic_plot('月刷卡额', tick2, 2)
economic_plot('个人月收入', tick3, 3)
economic_plot('家庭月收入', tick4, 4)
plt.show()

# 导入自行编写的绘制指定数量颜色的函数
from color import color, ncolors


# 编写个人月收入，家庭月收入与月刷卡额之间的关系函数
def risk_plot(column1, column2, xlabel_list=[], ylabel_list=[]):
    fig, ax = plt.subplots(figsize=(8, 6))  # 画布大小
    x_data = credit[column1]  # x轴数据
    co = list(map(lambda x: color(tuple(x)), ncolors(len(ylabel_list))))  # 指定数量的颜色

    # 循环绘制柱状堆叠图
    for i in sorted(x_data.unique()):
        y_data = credit[x_data == i][column2]
        part = sorted(y_data.unique())
        exp = 0
        if part[0] == 0:
            for j in part:
                exp1 = y_data.value_counts()[j] / len(y_data)
                ax.bar(i, exp1, bottom=exp, width=0.5, color=co[j], label=ylabel_list[j])
                exp += exp1
        else:
            for j in part:
                exp1 = y_data.value_counts()[j] / len(y_data)
                ax.bar(i, exp1, bottom=exp, width=0.5, color=co[j - 1], label=ylabel_list[j - 1])
                exp += exp1

    ax.set_xticks([i + 1 for i in range(len(x_data.unique()))])  # 重设x轴坐标数据
    ax.set_xticklabels(xlabel_list, fontsize=10)  # 设置x轴坐标显示数据
    ax.set_xlabel(column1 + '（万元）', fontsize=10)  # 设置x轴标题
    plt.ylabel('占比', fontsize=12)  # 设置y轴标题

    # 图例去重
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc=[1.01, 0], fontsize=10, title=column2 + '（万元）')

    # 调整子图位置
    fig.subplots_adjust(right=0.8)


print('\n')
risk_plot('个人月收入', '家庭月收入', ['无收入', '0~1', '1~2', '2~3', '3~4', '4~5', '5~6', '6以上'],
          ['未知', '2以下', '2~4', '4~6', '6~8', '8~10', '10以上'])
plt.show()
risk_plot('月刷卡额', '个人月收入', ['2以下', '2~4', '4~6', '6~8', '8~10', '10~15', '15~20', '20以上'],
          ['无收入', '0~1', '1~2', '2~3', '3~4', '4~5', '5~6', '6以上'])
plt.show()
risk_plot('月刷卡额', '家庭月收入', ['2以下', '2~4', '4~6', '6~8', '8~10', '10~15', '15~20', '20以上'],
          ['未知', '2以下', '2~4', '4~6', '6~8', '8~10', '10以上'])
plt.show()

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

carddata = pd.read_csv('./credit_card.csv', engine='python', encoding='GBK')

# 筛选逾期但是不是瑕疵户的数据
exp1 = (carddata['逾期'] == 1) & (carddata['瑕疵户'] == 2)
# 筛选呆账但是不是瑕疵户的数据
exp2 = (carddata['呆账'] == 1) & (carddata['瑕疵户'] == 2)
# 筛选有强制停卡记录但是不是瑕疵户的数据
exp3 = (carddata['强制停卡记录'] == 1) & (carddata['瑕疵户'] == 2)
# 筛选退票但是不是瑕疵户的数据
exp4 = (carddata['退票'] == 1) & (carddata['瑕疵户'] == 2)
# 筛选有拒收记录但是不是瑕疵户的数据
exp5 = (carddata['拒往记录'] == 1) & (carddata['瑕疵户'] == 2)
# 筛选有呆账但是没有拒收记录的数据
exp6 = (carddata['呆账'] == 1) & (carddata['拒往记录'] == 2)
# 筛选有强制停卡记录但是没有拒收记录的数据
exp7 = (carddata['强制停卡记录'] == 1) & (carddata['拒往记录'] == 2)
# 筛选退票但是没有拒收记录的数据
exp8 = (carddata['退票'] == 1) & (carddata['拒往记录'] == 2)
# 筛选频率为5但是月刷卡额大于1的数据
exp9 = (carddata['频率'] == 5) & (carddata['月刷卡额'] > 1)
# 筛选异常数据
Final = carddata.loc[(exp1 | exp2 | exp3 | exp4 | exp5 | exp6 | exp7 | exp8 | exp9).apply(lambda x: not (x)), :]
Final.reset_index(inplace=True)

# 个人月收入（万元）
PersonalMonthIncome = [0, 1, 2, 3, 4, 5, 6, 7, 8]
for i in range(8):
    Final.loc[Final['个人月收入'] == i + 1, '个人月收入'] = PersonalMonthIncome[i]
# 根据5 、6的情况计算个人月收入和家庭月收入的比值，确定家庭月收入为未知的情况
FamilyMonthIncome = [2, 4, 6, 8, 10, 12]
m = (Final.loc[:, '家庭月收入'] == 5)
Final.loc[m, '家庭月收入'] = FamilyMonthIncome[4]
ratio5 = Final.loc[m, '个人月收入'] / Final.loc[m, '家庭月收入']
m1 = Final.loc[:, '家庭月收入'] == 6
Final.loc[m1, '家庭月收入'] = FamilyMonthIncome[5]
ratio6 = Final.loc[m1, '个人月收入'] / Final.loc[m1, '家庭月收入']

# 家庭月收入（万元）
FamilyMonthIncome = [2, 4, 6, 8, 10, 15]
Final.loc[Final['家庭月收入'] == 0, '家庭月收入'] = 6
for i in range(6):
    m2 = Final.loc[:, '家庭月收入'] == i + 1
    Final.loc[m2, '家庭月收入'] = FamilyMonthIncome[i]

# 月刷卡额（万元）
MonthCardPay = [2, 4, 6, 8, 10, 15, 20, 25]
for i in range(8):
    m = Final.loc[:, '月刷卡额'] == i + 1
    Final.loc[m, '月刷卡额'] = MonthCardPay[i]

# 个人月开销（万元）
PersonalMonthOutcome = [1, 2, 3, 4, 6]
for i in range(5):
    m = Final['个人月开销'] == i + 1
    Final.loc[m, '个人月开销'] = PersonalMonthOutcome[i]


# 属性值为1（是）的记为1分，属性值为2（否）的记为0分
def GetScore(x):
    if x == 2:
        a = 0
    else:
        a = 1
    return (a)


BuguserSocre = Final['瑕疵户'].apply(GetScore)
OverdueScore = Final['逾期'].apply(GetScore)
BaddebtScore = Final['呆账'].apply(GetScore)
CardstopedScore = Final['强制停卡记录'].apply(GetScore)
BounceScore = Final['退票'].apply(GetScore)
RefuseScore = Final['拒往记录'].apply(GetScore)
Final['历史信用风险'] = (BuguserSocre + OverdueScore * 2 + BaddebtScore * 3
                         + CardstopedScore * 3 + BounceScore * 3 + RefuseScore * 3)

# 月刷卡额/个人月收入
CardpayPersonal = Final['月刷卡额'] / Final['个人月收入']
# 月刷卡额/家庭月收入
CardpayFamily = Final['月刷卡额'] / Final['家庭月收入']
EconomicScore = []
for i in range(Final.shape[0]):
    if CardpayPersonal[i] <= 1:
        if Final.loc[i, '借款余额'] == 1:
            EconomicScore.append(1)
        else:
            EconomicScore.append(0)

    if CardpayPersonal[i] > 1:
        if CardpayFamily[i] <= 1:
            if Final.loc[i, '借款余额'] == 1:
                EconomicScore.append(2)
            else:
                EconomicScore.append(1)

    if CardpayFamily[i] > 1:
        if Final.loc[i, '借款余额'] == 1:
            EconomicScore.append(4)
        else:
            EconomicScore.append(2)

# 个人月开销/月刷卡额
OutcomeCardpay = Final['个人月开销'] / Final['月刷卡额']
OutcomeCardpayScore = []
for i in range(Final.shape[0]):
    if (OutcomeCardpay[i] <= 1):
        OutcomeCardpayScore.append(1)
    else:
        OutcomeCardpayScore.append(0)

Final['经济风险情况'] = np.array(EconomicScore) + np.array(OutcomeCardpayScore)

# 判断用户是否具有稳定的收入
HouseScore = []
for i in range(Final.shape[0]):
    if 3 <= Final.loc[i, '住家'] <= 5:
        HouseScore.append(0)
    else:
        HouseScore.append(1)

JobScore = []
for i in range(Final.shape[0]):
    if (Final.loc[i, '职业'] <= 7 | Final.loc[i, '职业'] == 19 |
            Final.loc[i, '职业'] == 21):
        JobScore.append(2)
    if (Final.loc[i, '职业'] >= 8 & Final.loc[i, '职业'] <= 11):
        JobScore.append(1)
    if (Final.loc[i, '职业'] <= 18 & Final.loc[i, '职业'] >= 12 |
            Final.loc[i, '职业'] == 20 | Final.loc[i, '职业'] == 22):
        JobScore.append(0)

AgeScore = []
for i in range(Final.shape[0]):
    if Final.loc[i, '年龄'] <= 2:
        AgeScore.append(1)
    else:
        AgeScore.append(0)

Final.loc[:,'收入风险情况'] = np.array(HouseScore) + np.array(JobScore) + np.array(AgeScore)

StdScaler = StandardScaler().fit(Final[['历史信用风险', '经济风险情况', '收入风险情况']])
ScoreModel = StdScaler.transform(Final[['历史信用风险', '经济风险情况', '收入风险情况']])
