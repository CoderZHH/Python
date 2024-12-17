import pandas as pd

media = pd.read_csv('./data/media_index.csv', encoding='gbk', header='infer')

# 将高清替换为空
media['station_name'] = media['station_name'].str.replace('-高清', '')

# 过滤特殊线路用户
media = media.loc[(media.owner_code != 2) & (media.owner_code != 9) & (media.owner_code != 10), :]
print('查看过滤后的特殊线路的用户:', media.owner_code.unique())

# 删除政企用户
media = media.loc[(media.owner_name != 'EA级') & (media.owner_name != 'EB级') &
                  (media.owner_name != 'EC级') & (media.owner_name != 'ED级') &
                  (media.owner_name != 'EE级'), :]
print('查看过滤后的政企用户:', media.owner_name.unique())

# 对开始时间进行拆分
type(media.loc[0, 'origin_time'])  # 检查数据类型
# 转化为时间类型
media['end_time'] = pd.to_datetime(media['end_time'])
media['origin_time'] = pd.to_datetime(media['origin_time'])
# 提取秒
media['origin_second'] = media['origin_time'].dt.second
media['end_second'] = media['end_time'].dt.second
# 筛选数据（删除开始时间和结束观看时间单位秒为0的数据）
ind1 = (media['origin_second'] == 0) & (media['end_second'] == 0)
media1 = media.loc[~ind1, :]

# 基于开始时间和结束时间的记录去重
media1.end_time = pd.to_datetime(media1.end_time)
media1.origin_time = pd.to_datetime(media1.origin_time)
media1 = media1.drop_duplicates(['origin_time', 'end_time'])

# 隔夜处理
# 去除开始时间，结束时间为空值的数据
media1 = media1.loc[media1.origin_time.dropna().index, :]
media1 = media1.loc[media1.end_time.dropna().index, :]
# 建立各星期的数字标记
media1['星期'] = media1.origin_time.apply(lambda x: x.weekday() + 1)
dic = {1: '星期一', 2: '星期二', 3: '星期三', 4: '星期四', 5: '星期五', 6: '星期六', 7: '星期日'}
for i in range(1, 8):
    ind = media1.loc[media1['星期'] == i, :].index
    media1.loc[ind, '星期'] = dic[i]
# 查看有多少观看记录是隔夜的，隔夜的进行隔夜处理
a = media1.origin_time.apply(lambda x: x.day)
b = media1.end_time.apply(lambda x: x.day)
sum(a != b)
media2 = media1.loc[a != b, :].copy()  # 需要做隔夜处理的数据


# 定义一个函数，将跨夜的收视数据分为两天
def geyechuli_Weeks(x):
    dic = {'星期一': '星期二', '星期二': '星期三', '星期三': '星期四', '星期四': '星期五',
           '星期五': '星期六', '星期六': '星期日', '星期日': '星期一'}
    return x.apply(lambda y: dic[y.星期], axis=1)


media1.loc[a != b, 'end_time'] = media1.loc[a != b, 'end_time'].apply(lambda x:
                                                                      pd.to_datetime('%d-%d-%d 23:59:59' % (
                                                                      x.year, x.month, x.day)))
media2.loc[:, 'origin_time'] = pd.to_datetime(media2.end_time.apply(lambda x:
                                                                    '%d-%d-%d 00:00:01' % (x.year, x.month, x.day)))
media2.loc[:, '星期'] = geyechuli_Weeks(media2)
media3 = pd.concat([media1, media2])
media3['origin_time1'] = media3.origin_time.apply(lambda x:
                                                  x.second + x.minute * 60 + x.hour * 3600)
media3['end_time1'] = media3.end_time.apply(lambda x:
                                            x.second + x.minute * 60 + x.hour * 3600)
media3['wat_time'] = media3.end_time1 - media3.origin_time1  # 构建观看总时长属性

# 清洗时长不符合的数据
# 剔除下次观看的开始时间小于上一次观看的结束时间的记录
media3 = media3.sort_values(['phone_no', 'origin_time'])
media3 = media3.reset_index(drop=True)
a = [media3.loc[i + 1, 'origin_time'] < media3.loc[i, 'end_time'] for i in range(len(media3) - 1)]
a.append(False)
aa = pd.Series(a)
media3 = media3.loc[~aa, :]

# 去除小于4S的记录
media3 = media3.loc[media3['wat_time'] > 4, :]
media3.to_csv('./tmp/media3.csv', na_rep='NaN', header=True, index=False)
