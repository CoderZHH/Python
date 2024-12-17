#1.基于物品的协同过滤推荐模型评价
#接着代码10-8
score = rec['T/F'].value_counts()['T']/(rec['T/F'].value_counts()['T']+rec['T/F'].value_counts()['F'])
print('推荐的准确率为：',str(round(score*100,2))+'%')      

#基于流行度算法的模型评价
# 接着代码10-9
recommend_dataframe = recommend_dataframe
import numpy as np
phone_no = media6_test['phone_no'].unique()
real_dataframe = pd.DataFrame()
pre = pd.DataFrame(np.zeros((len(phone_no), 3)), columns=['phone_no', 'pre_num', 're_num'])
for i in range(len(phone_no)):
    real = media6_test.loc[media6_test['phone_no'] == phone_no[i], 'program_title']
    a = recommend_dataframe['program'].isin(real)
    pre.iloc[i, 0] = phone_no[i]
    pre.iloc[i, 1] = sum(a)
    pre.iloc[i, 2] = len(real)
    real_dataframe = pd.concat([real_dataframe, real])

real_program = np.unique(real_dataframe.iloc[:, 0])
# 计算推荐准确率
precesion = (sum(pre['pre_num'] / m)) / len(pre)  # m为推荐个数，为3000
print('流行度推荐的准确率为：', str(round(precesion*100,2))+'%')