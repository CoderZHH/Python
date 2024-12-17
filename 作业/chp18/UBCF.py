import pandas as pd
import numpy as np
# 编写UCF推荐算法
def UBCF_rec(train_df,s_data,N):
    rec_pre = pd.DataFrame()
    for u in s_data.index:
        # 获取推荐电影
        try:
            s_users = s_data.loc[u].dropna().sort_values().index[int('-'+str(N)):]
            s_items = []
            for v in s_users:
                s_items += list(train_df.loc[[v]].dropna(axis=1).columns)
            u_items = train_df.loc[u].dropna().index
            rec_items = list(set([i for i in s_items if i not in u_items]))

            # 获取预测评分
            s_uv = s_data.loc[u,list(s_users)].values
            train_df_tmp = train_df.loc[s_users,rec_items].values
            r_m = np.nanmean(train_df.loc[s_users],axis=1)
            U_array = (train_df_tmp-(r_m.reshape(-1,1)*np.ones((N,train_df_tmp.shape[1]))))*s_uv.reshape(-1,1)
            U = np.nansum(U_array,axis=0)   
            s_uv_tmp = s_uv.reshape(-1,1)*np.ones((len(s_users),train_df_tmp.shape[1]))*(train_df_tmp/train_df_tmp)
            D = np.nansum(s_uv_tmp*r_m.reshape(-1,1),axis=0)
            D = np.nansum(s_uv_tmp,axis=0)
            p = np.mean(r_m) + U/D
            rec_pre_tmp = pd.DataFrame(columns=rec_items)
            rec_pre_tmp.loc[u,:]=p
            rec_pre = pd.concat([rec_pre,rec_pre_tmp])
        except:
            pass
    return rec_pre
