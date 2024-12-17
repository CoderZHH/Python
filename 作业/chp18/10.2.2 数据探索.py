#1.分布分析
#（1）用户观看总时长
import pandas as pd
import matplotlib.pyplot as plt
media3 = pd.read_csv('./tmp/media3.csv', header='infer')
# 计算用户观看总时长
m = pd.DataFrame(media3['wat_time'].groupby([media3['phone_no']]).sum())
m = m.sort_values(['wat_time'])
m = m.reset_index()
m['wat_time'] = m['wat_time'] / 3600

# 绘制观看用户的观看总时长柱形图
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为SimHei显示中文
plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示符号
plt.figure(figsize=(8, 4))
plt.bar(m.index,m.iloc[:,1])
plt.xlabel('观看用户')
plt.ylabel('观看时长（小时）')
plt.title('用户观看总时长')
plt.show()

#（2）付费频道与点播回看的周观看时长
import re
# 计算周观看时长
n = pd.DataFrame(media3['wat_time'].groupby([media3['星期']]).sum())
n = n.reset_index()
n = n.loc[[0, 2, 1, 5, 3, 4, 6], :]
n['wat_time'] = n['wat_time'] / 3600

# 绘制周观看时长分布折线图
plt.figure(figsize=(8, 4))
plt.plot(range(7), n.iloc[:, 1])
plt.xticks([0, 1, 2, 3, 4, 5, 6], 
           ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'])
plt.xlabel('星期')
plt.ylabel('观看时长（小时）')
plt.title('周观看时长分布')
plt.show()

# 计算付费频道与点播回看的周观看时长
media_res = media3.loc[media3['res_type']==1, :]
ffpd_ind = [re.search('付费', str(i))!=None for i in media3.loc[:, 'station_name']]
media_ffpd = media3.loc[ffpd_ind, :]
z = pd.concat([media_res, media_ffpd], axis=0)
z = z['wat_time'].groupby(z['星期']).sum()
z = z.reset_index()
z = z.loc[[0, 2, 1, 5, 3, 4, 6], :]
z['wat_time'] = z['wat_time'] / 3600

# 绘制付费频道与点播回看的周观看时长分布折线图
plt.figure(figsize=(8, 4))
plt.plot(range(7), z.iloc[:, 1])
plt.xticks([0, 1, 2, 3, 4, 5, 6], 
           ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'])
plt.xlabel('星期')
plt.ylabel('观看时长（小时）')
plt.title('付费频道与点播回看的周观看时长分布')
plt.show()

#2.对比分析
import re
# 计算工作日与周末的观看总时长占比
ind = [re.search('星期六|星期日', str(i))!=None for i in media3['星期']]
freeday = media3.loc[ind, :]
workday = media3.loc[[ind[i]==False for i in range(len(ind))], :]
m1 = pd.DataFrame(freeday['wat_time'].groupby([freeday['phone_no']]).sum())
m1 = m1.sort_values(['wat_time'])
m1 = m1.reset_index()
m1['wat_time'] = m1['wat_time'] / 3600
m2 = pd.DataFrame(workday['wat_time'].groupby([workday['phone_no']]).sum())
m2 = m2.sort_values(['wat_time'])
m2 = m2.reset_index()
m2['wat_time'] = m2['wat_time'] / 3600
w = sum(m2['wat_time']) / 5
f = sum(m1['wat_time']) / 2

# 绘制工作日与周末的观看总时长占比饼图
colors = ['bisque', 'lavender']
plt.figure(figsize=(6, 6))
plt.pie([w, f], labels=['工作日', '周末'], 
        explode=[0.1, 0.1], autopct='%1.1f%%', 
        colors=colors, labeldistance=1.05, textprops={'fontsize': 15})
plt.title('工作日与周末观看总时长占比', fontsize=15)
plt.show()

# 绘制周末观看总时长分布柱形图
plt.figure(figsize=(12, 6))
plt.subplot(121)  # 将figure分成1*2=2个子图区域，第3个参数1表示将生成的图画放在第1个位置
plt.bar(m1.index, m1.iloc[:, 1])
plt.xlabel('观看用户')
plt.ylabel('观看时长（小时）')
plt.title('周末用户观看总时长')

# 绘制工作日观看总时长分布柱形图
plt.subplot(122)  # 同理，将生成的图画放在第2个位置
plt.bar(m2.index, m2.iloc[:, 1])
plt.xlabel('观看用户')
plt.ylabel('观看时长（小时）')
plt.title('工作日用户观看总时长')
plt.show()

#3.贡献度分析
# 计算所有收视频道的观看时长与观看次数
media3.station_name.unique()
pindao = pd.DataFrame(media3['wat_time'].groupby([media3.station_name]).sum())
pindao = pindao.sort_values(['wat_time'])
pindao = pindao.reset_index()
pindao['wat_time'] = pindao['wat_time'] / 3600
pindao_n = media3['station_name'].value_counts()
pindao_n = pindao_n.reset_index()
pindao_n.columns = ['station_name', 'counts']
a = pd.merge(pindao, pindao_n, left_on='station_name', right_on ='station_name', how='left')

# 绘制所有频道号的观看时长柱形图和观看次数折线图的组合图
fig, left_axis = plt.subplots()
right_axis = left_axis.twinx()
left_axis.bar(a.index, a.iloc[:, 1])
right_axis.plot(a.index, a.iloc[:, 2], 'r.-')
left_axis.set_ylabel('观看时长（小时）')
right_axis.set_ylabel('观看次数')
left_axis.set_xlabel('频道号')
plt.xticks([])
plt.title('所有收视频道号的观看时长与观看次数')
plt.tight_layout()
plt.show()

# 绘制收视排名前15的频道名称的观看时长柱形图
plt.figure(figsize=(15, 8))
plt.bar(range(15), pindao.iloc[124:139, 1])
plt.xticks(range(15), pindao.iloc[124:139, 0])
plt.xlabel('频道名称')
plt.ylabel('观看时长（小时）')
plt.title('收视排名前15频道名称的观看时长')
plt.show()


