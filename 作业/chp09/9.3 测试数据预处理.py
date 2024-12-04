import pandas as pd
import numpy as np
# 读取测试样本
data = pd.read_csv('../data/test.csv')

# 处理data_received属性并转为时间类型
data['date_received'] = data['date_received'].astype('str').apply(
        lambda x:x.split('.')[0])
data['date_received'] = pd.to_datetime(data['date_received'])

# 处理date属性并转为时间类型
data['date'] = data[ 'date'].astype('str').apply(lambda x:x.split('.')[0])
data['date'] = pd.to_datetime(data['date'])

# 自定义discount函数处理优惠率属性
data['discount_rate'] = data['discount_rate'].fillna('null')
def discount(x):
    if ':' in x :
        split = x.split(':')
        discount_rate = (int(split[0])-int(split[1]))/int(split[0])
        return round(discount_rate, 2)
    elif x == 'null':
        return np.nan
    else :
        return float(x) 
# 调用discount函数将满减优惠改写成折扣率形式
data['discount_rate'] = data['discount_rate'].map(discount)

# 标记样本
# 建立训练样本分类标签,-1代表普通样本，1代表正样本， 0代表负样本
data["label"] = 0  # 创建一个列值为0，
data.loc[data['coupon_id'].isnull(), 'label']=-1  #普通样本-1
data.loc[(data['date']-data['date_received']).dt.days<=15, 'label']=1  # 正样本1

# 构建指标
quality = data.copy()
# 导入自定义特征包feature_name构建用户、商户、优惠券、交互相关指标
from feature_name import feature_name
data_user, data_merchant, data_coupon, data_mutual = feature_name(
    train_quality=quality)

# 对构建后的用户、商户、优惠券、交互相关指标进行数据拼接
# 对样本与指标类型表进行拼接
merge = pd.merge(data_user, quality, on='user_id')
merge = pd.merge(merge, data_merchant, on="merchant_id")
merge = pd.merge(merge, data_coupon, on='merchant_id')
clean_test = pd.merge(merge, data_mutual, on=['user_id','merchant_id'])
clean_test.isnull().sum()  # 统计缺失值
clean_test.fillna(0)  # 缺失值填充
print('构建指标后测试样本的形状：', clean_test.shape[0])

# 写出数据
clean_test.to_csv('../tmp/clean_test.csv', index=False)

