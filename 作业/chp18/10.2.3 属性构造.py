import pandas as pd
import numpy as np
import re

media3 = pd.read_csv('./tmp/media3.csv', header='infer')

# 1.构建家庭成员标签
live_label = pd.read_csv('./data/table_livelabel.csv', encoding='gbk')
# 时间列存在很多种写法，而且存在隔天的情况
live_label.开始时间 = pd.to_datetime(live_label.开始时间, format='%Y-%m-%d %H:%M:%S', errors='coerce')
# 将时间列变成datetime类型，好比较大小
live_label.结束时间 = pd.to_datetime(live_label.结束时间, format='%Y-%m-%d %H:%M:%S', errors='coerce')
live_label['origin_time1'] = live_label.开始时间.apply(lambda x:
                                                       x.second + x.minute * 60 + x.hour * 3600)
live_label['end_time1'] = live_label.结束时间.apply(lambda x:
                                                    x.second + x.minute * 60 + x.hour * 3600)
print('查看星期:', live_label.星期.unique())

# 有些节目跨夜，需进行隔夜处理
def geyechuli_xingqi(x):
    dic = {'星期一': '星期二', '星期二': '星期三', '星期三': '星期四', '星期四': '星期五',
           '星期五': '星期六', '星期六': '星期日', '星期日': '星期一'}
    return x.apply(lambda y: dic[y.星期], axis=1)

ind1 = live_label.结束时间 < live_label.开始时间
label1 = live_label.loc[ind1, :].copy()
# 日期可以变，后面以end_time比较
live_label.loc[ind1, '结束时间'] = pd.Timestamp('2018-06-07 23:59:59')
live_label.loc[ind1, 'end_time1'] = 24 * 3600
label1.iloc[:, 1] = pd.Timestamp('2018-06-07 00:00:00')
label1.iloc[:, -2] = 0
label1.iloc[:, 0] = geyechuli_xingqi(label1)
label = pd.concat([live_label, label1])
label = label.reset_index(drop=True)  # 恢复默认索引

data_pindao = media3.copy()
label_ = label.loc[:, ['星期', 'origin_time1', 'end_time1', '频道', '适用人群']]
label_.columns = ['星期', 'origin_time1', 'end_time1', 'station_name', '适用人群']
media_ = data_pindao.loc[:, ['phone_no', '星期', 'origin_time1',
                             'end_time1', 'station_name', ]]
family_ = pd.merge(media_, label_, how='left', on=['星期', 'station_name'])
f = np.array(family_.loc[:, ['origin_time1_x', 'end_time1_x', 'origin_time1_y', 'end_time1_y']])

# lebel中的栏目记录分为四类：一类是只看了后半截，一类是全部都看了，
# 一类是只看了前半截，一类是看了中间一截
n1 = np.apply_along_axis(lambda x:
                         (x[0] > x[2]) & (x[0] < x[3]) & (x[1] >= x[3]), 1, f)  # 1是行，2是列
n2 = np.apply_along_axis(lambda x:
                         ((x[0] <= x[2]) & (x[1] >= x[3])), 1, f)
n3 = np.apply_along_axis(lambda x:
                         ((x[1] > x[2]) & (x[1] < x[3]) & (x[0] <= x[2])), 1, f)
n4 = np.apply_along_axis(lambda x:
                         ((x[0] > x[2]) & (x[1] < x[3])), 1, f)
da1 = family_.loc[n1, :].copy()
da1['wat_time'] = da1.end_time1_y - da1.origin_time1_x
da2 = family_.loc[n2, :].copy()
da2['wat_time'] = da2.end_time1_y - da2.origin_time1_y
da3 = family_.loc[n3, :].copy()
da3['wat_time'] = da3.end_time1_x - da3.origin_time1_y
da4 = family_.loc[n4, :].copy()
da4['wat_time'] = da4.end_time1_x - da4.origin_time1_x
sd = pd.concat([da1, da2, da3, da4])
grouped = pd.DataFrame(sd['wat_time'].groupby([sd['phone_no'], sd['适用人群']]).sum())
grouped1 = pd.DataFrame(data_pindao['wat_time'].groupby([data_pindao['phone_no']]).sum())
phone_no = []
for i in range(len(grouped)):
    id = grouped.index[i][0]
    if id in grouped1.index:
        shang = grouped['wat_time'].iloc[i] / grouped1.loc[grouped1.index == id, 'wat_time'].values[0]
        if shang > 0.16:
            phone_no.append(grouped.index[i][0])
    else:
        continue
grouped2 = grouped.reset_index()

# 2.找出满足0.16标准的用户的家庭成员
aaa = pd.DataFrame(np.zeros([0, 3]), columns=grouped2.columns)
for k in phone_no:
    aaa = pd.concat([aaa, grouped2.loc[grouped2.iloc[:, 0] == k, :]], axis=0)
a = [aaa.loc[aaa['phone_no'] == k, '适用人群'].tolist() for k in aaa['phone_no'].unique()]
a = pd.Series([pd.Series(a[i]).unique() for i in range(len(a))])
a = pd.DataFrame(a)
b = pd.DataFrame(aaa['phone_no'].unique())
c = pd.concat([a, b], axis=1)
c.columns = ['家庭成员', 'phone_no']
grouped1 = grouped1.reset_index()
users_label = pd.merge(grouped1, c, left_on='phone_no', right_on='phone_no', how='left')

# 3.构建电视依赖度标签
di = media3.phone_no.value_counts().values < 10
users_label['电视依赖度'] = 0
users_label.loc[di, '电视依赖度'] = '低'
zhong_gao = [i for i in users_label.index if i not in di]
num = media3.phone_no.value_counts()
for i in zhong_gao:
    if (users_label.loc[i, 'wat_time'] / num.iloc[i]) <= 3000:
        users_label.loc[i, '电视依赖度'] = '中'
users_label.loc[users_label.电视依赖度 == 0, '电视依赖度'] = '高'

# 4.构建机顶盒名称标签
jidinghe = media3.loc[media3['res_type'] == 1, :]
jdh = jidinghe.res_name.groupby(jidinghe.phone_no).unique()
jdh = jdh.reset_index()
jdh.columns = ['phone_no', '机顶盒名称']
users_label = pd.merge(users_label, jdh, left_on='phone_no', right_on='phone_no', how='left')

# 5.观看时间偏好（周末）
media_watch = media3.loc[:, ['phone_no', 'origin_time', 'end_time', 'res_type',
                             '星期', 'wat_time']]
media_f1 = media_watch.loc[media_watch['星期'] == '星期六', :]
media_f2 = media_watch.loc[media_watch['星期'] == '星期日', :]
media_freeday = pd.concat([media_f1, media_f2], axis=0)
media_freeday = media_freeday.reset_index(drop=True)  # 恢复默认索引

# 分割日期和时间，按空格号分开
T1 = [str(media_freeday.iloc[i, 1]).split(' ') for i in list(media_freeday.index)]
media_freeday['origin_time'] = [' '.join(['2018/06/09', T1[i][1]]) for i in media_freeday.index]
media_freeday['origin_time'] = pd.to_datetime(media_freeday['origin_time'],
                                              format='%Y/%m/%d %H:%M', errors='coerce')
point = ['2018/06/09 00:00:00', '2018/06/09 06:00:00', '2018/06/09 09:00:00',
         '2018/06/09 11:00:00', '2018/06/09 14:00:00', '2018/06/09 16:00:00',
         '2018/06/09 18:00:00', '2018/06/09 22:00:00', '2018/06/09 23:59:59']
lab = ['凌晨', '早晨', '上午', '中午', '下午', '傍晚', '晚上', '夜晚']
media_freeday['时间偏好'] = np.nan
for i in media_freeday.index:
    data = media_freeday.loc[i, 'origin_time']
    for j in range(len(point) - 1):
        if point[j] <= str(data) <= point[j + 1]:
            media_freeday.loc[i, '时间偏好'] = lab[j]
# 合并到主数据中
users_label = pd.merge(users_label, media_freeday[['phone_no', '时间偏好']], on='phone_no', how='left')

# 6.构建付费频道月均收视时长标签
import re

ffpd_ind = [re.search('付费', str(i)) != None for i in media3.loc[:, 'station_name']]
media_ffpd = media3.loc[ffpd_ind, :]
ffpd = media_ffpd['wat_time'].groupby(media_ffpd['phone_no']).sum()
ffpd = ffpd.reset_index()  # 增加索引
ffpd['付费频道月均收视时长'] = 0
for i in range(len(ffpd)):
    if ffpd.iloc[i, 1] < 3600:
        ffpd.iloc[i, 2] = '付费频道月均收视时长短'
    elif 3600 <= ffpd.iloc[i, 1] <= 7200:
        ffpd.iloc[i, 2] = '付费频道月均收视时长中'
    else:
        ffpd.iloc[i, 2] = '付费频道月均收视时长长'
ffpd = ffpd.loc[:, ['phone_no', '付费频道月均收视时长']]
users_label = pd.merge(users_label, ffpd, left_on='phone_no',
                       right_on='phone_no', how='left')
ffpd_ind = [str(users_label.iloc[i, 6]) == 'nan' for i in users_label.index]
users_label.loc[ffpd_ind, 6] = '付费频道无收视'

# 7.构建点播回看月均收视时长标签
media_res = media3.loc[media3['res_type'] == 1, :]
res = media_res['wat_time'].groupby(media_res['phone_no']).sum()
res = res.reset_index()  # 增加索引
res['点播回看月均收视时长'] = 0
for i in range(len(res)):
    if res.iloc[i, 1] < 10800:
        res.iloc[i, 2] = '点播回看月均收视时长短'
    elif 10800 <= res.iloc[i, 1] <= 36000:
        res.iloc[i, 2] = '点播回看月均收视时长中'
    else:
        res.iloc[i, 2] = '点播回看月均收视时长长'
res = res.loc[:, ['phone_no', '点播回看月均收视时长']]
users_label = pd.merge(users_label, res, left_on='phone_no',
                       right_on='phone_no', how='left')
res_ind = [str(users_label.iloc[i, 7]) == 'nan' for i in users_label.index]
users_label.loc[res_ind, 7] = '点播回看无收视'

# 8.体育偏好
media3.loc[media3['program_title'] == 'a', 'program_title'] = \
    media3.loc[media3['program_title'] == 'a', 'vod_title']
program = [re.sub('\(.*', '', i) for i in media3['program_title']]  # 去除集数
program = [re.sub('.*月.*日', '', str(i)) for i in program]  # 去除日期
program = [re.sub('^ ', '', str(i)) for i in program]  # 前面的空格
program = [re.sub('\\d+$', '', i) for i in program]  # 去除结尾数字
program = [re.sub('【.*】', '', i) for i in program]  # 去除方括号内容
program = [re.sub('第.*季.*', '', i) for i in program]  # 去除季数
program = [re.sub('广告|剧场', '', i) for i in program]  # 去除广告、剧场字段
media3['program_title'] = program
ind = [media3.loc[i, 'program_title'] != '' for i in media3.index]
media_ = media3.loc[ind, :]
media_ = media_.drop_duplicates()  # 去重
media_.to_csv('./tmp/media4.csv', na_rep='NaN', header=True, index=False)