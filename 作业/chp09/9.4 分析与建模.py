import pandas as pd
import numpy as np
# 读取数据
train = pd.read_csv('../tmp/clean_train.csv')
test = pd.read_csv('../tmp/clean_test.csv')
# 抽取正负样本
train = train[train['label'] == 1].sample(sum(train['label'] == 1)).append(
    train[train['label'] == 0].sample(sum(train['label'] == 0)))
test = test[test['label'] == 1].sample(sum(test['label'] == 1)).append(
    test[test['label'] == 0].sample(sum(test['label'] == 0)))

# 删除列
x_train = train.drop(['user_id', 'merchant_id', 'coupon_id',
                      'date_received', 'date'], axis=1)
x_test = test.drop(['user_id', 'merchant_id', 'coupon_id',
                    'date_received', 'date', 'label'], axis=1)
# 处理无穷数据（无穷数据大或者无穷数据小）
x_train[np.isinf(x_train)] = 0
x_test[np.isinf(x_test)] = 0

# 决策树分类模型
from sklearn.tree import DecisionTreeClassifier
model_dt1 = DecisionTreeClassifier(max_leaf_nodes=16, random_state=123).fit(
        x_train.drop(['label'], axis=1), x_train['label'])

# 模型预测
pre_dt = model_dt1.predict(x_test)

# dt_class存放决策树分类预测结果
dt_class = test[['user_id', 'merchant_id', 'coupon_id']]
dt_class['class'] = pre_dt
# 写出决策树分类预测结果
dt_class.to_csv('../tmp/dt_class.csv', index=False)


# 梯度提升分类模型
from sklearn.ensemble import GradientBoostingClassifier
# 构建模型
model = GradientBoostingClassifier(n_estimators=100, max_depth=5)
# 模型训练
model.fit(x_train.drop(['label'], axis=1), x_train['label'])
# 模型预测
pre_gb = model.predict(x_test)

# gb_class存放梯度提升预测结果
gb_class = test[['user_id', 'merchant_id', 'coupon_id']]
gb_class['class'] = pre_gb
# 写出梯度提升预测结果
gb_class.to_csv('../tmp/gb_class.csv', index=False)


# XGBoost分类模型
import xgboost as xgb
model_test = xgb.XGBClassifier(max_depth=6, learning_rate=0.1, n_estimators=150,
                          silent=True, objective='binary:logistic')
# max_depth是数的最大深度，默认值为6，避免过拟合
# learning_rate为学习率，n_estimators为总共迭代的次数，即决策树的个数，silent为中间过程
# binary:logistic 二分类的逻辑回归，返回预测的概率(不是类别)

# 模型训练
model_test.fit(x_train.drop(['label'], axis=1), x_train['label'])

# 模型预测
y_pred = model_test.predict(x_test)

# xgb_class存放xgboost预测结果
xgb_class = test[['user_id', 'merchant_id', 'coupon_id']]
xgb_class['class'] = y_pred
# 写出xgboost预测结果
xgb_class.to_csv('../tmp/xgb_class.csv', index=False)

