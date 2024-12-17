import pandas as pd
import numpy as np
media4 = pd.read_csv('../tmp/media4.csv', header='infer')

# 基于物品的协同过滤算法
m = media4.loc[:, ['phone_no', 'program_title']]
n = 500000
media5 = m.iloc[:n, :]
media5['value'] = 1
media5.drop_duplicates(['phone_no','program_title'],inplace=True)

from sklearn.model_selection import train_test_split
# 将数据划分为训练集测试集
media_train, media_test = train_test_split(media5, test_size=0.2, random_state=123)

# 长表转宽表，即用户-物品矩阵
train_df = media_train.pivot(index='phone_no', columns='program_title',values = 'value')  # 透视表
ui_matrix_tr = train_df
ui_matrix_tr.fillna(0,inplace = True)

test_df = media_test.pivot(index='phone_no', columns='program_title',values='value')  # 透视表
test_tmp = media_test.sample(frac=1000/media_test.shape[0],random_state=3)

# 求物品相似度矩阵
t=0
item_matrix_tr = pd.DataFrame(0, index=ui_matrix_tr.columns, columns=ui_matrix_tr.columns)
for i in item_matrix_tr.index:
    item_tmp = ui_matrix_tr[[i]].values*np.ones((ui_matrix_tr.shape[0],ui_matrix_tr.shape[1]))+ui_matrix_tr
    U = np.sum(item_tmp==2)
    D = np.sum(item_tmp!=0)
    item_matrix_tr.loc[i,:] = U/D
    t+=1
    if t%500==0:
        print(t)
    
# 将物品相似度矩阵对角线处理为零
for i in item_matrix_tr.index:
    item_matrix_tr.loc[i, i] = 0

# 获取推荐列表和模型评价
rec = pd.DataFrame(index=test_tmp.index, columns=['phone_no', '已观看节目', '推荐节目', 'T/F'])
rec.loc[:, 'phone_no'] = list(test_tmp.iloc[:, 0])
rec.loc[:, '已观看节目'] = list(test_tmp.iloc[:, 1])
# 开始推荐
for i in rec.index:
    try:
        usid = test_tmp.loc[i,'phone_no']
        animeid = test_tmp.loc[i,'program_title']
        item_anchor = list(ui_matrix_tr.loc[usid][ui_matrix_tr.loc[usid]==1].index)
        co = [j for j in item_matrix_tr.columns if j not in item_anchor]
        item_tmp = item_matrix_tr.loc[animeid,co]
        rec_anime = list(item_tmp.index)[item_tmp.argmax()]
        rec.loc[i, '推荐节目'] = rec_anime
        if test_df.loc[usid,rec_anime]==1:
            rec.loc[i,'T/F']='T'
        else:
            rec.loc[i,'T/F']='F'
    except:
        pass

# 保存推荐结果
rec.to_csv('../tmp/rec.csv')     
