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
                    '类别数', '极差', '四分位差', '众数', '方差', '偏度', '峰度'])

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
    ax.set_xlabel(column+'（万元）', fontsize=14)  # y轴坐标轴标题
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
    co = list(map(lambda x:color(tuple(x)), ncolors(len(ylabel_list))))  # 指定数量的颜色

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
                ax.bar(i, exp1, bottom=exp, width=0.5, color=co[j-1], label=ylabel_list[j-1])
                exp += exp1

    ax.set_xticks([i+1 for i in range(len(x_data.unique()))])  # 重设x轴坐标数据
    ax.set_xticklabels(xlabel_list, fontsize=10)  # 设置x轴坐标显示数据
    ax.set_xlabel(column1 + '（万元）', fontsize=10)  # 设置x轴标题
    plt.ylabel('占比', fontsize=12)  # 设置y轴标题

# 图例去重
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc=[1.01, 0], fontsize=10, title=column2+'（万元）')

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

