from sklearn.metrics import precision_score, roc_auc_score, roc_curve
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt

train_class = pd.read_csv('../tmp/clean_train.csv')  # 已预处理和贴标签训练数据
test_class = pd.read_csv('../tmp/clean_test.csv')  # 已预处理和贴标签测试数据
# 抽取正负样本
train_class = train_class[train_class['label'] == 1].sample(sum(train_class[
              'label'] == 1)).append(train_class[train_class['label'] == 0].sample(
              sum(train_class['label'] == 0)))
test_class = test_class[test_class['label'] == 1].sample(sum(test_class[
              'label'] == 1)).append(test_class[test_class['label'] == 0].sample(
              sum(test_class['label'] == 0)))
# 删除列
x_train = train_class.drop(['user_id', 'merchant_id', 'coupon_id',
                            'date_received', 'date'], axis=1)
x_test = test_class.drop(['user_id', 'merchant_id', 'coupon_id',
                          'date_received', 'date'], axis=1)
# 处理无穷数据(无穷数据大或者无穷数据小)
x_train[np.isinf(x_train)] = 0
x_test[np.isinf(x_test)] = 0

# 决策树分类模型
model_dt_evaluate = DecisionTreeClassifier(max_leaf_nodes=16,
    random_state=123).fit(x_train.drop(['label'], axis=1), x_train['label'])
model_dt_pre = model_dt_evaluate.predict(x_test.drop(['label'], axis=1))  # 模型预测

# 决策树分类模型评价指标值
pre = model_dt_evaluate.predict_proba(x_test.drop(['label'], axis=1))  # 输出预测概率
auc = roc_auc_score(x_test['label'], pre[:, 1])  # 计算AUC值
print('AUC值为%.2f%%:'% (auc * 100.0))
dt_evaluate_accuracy = accuracy_score(x_test['label'], model_dt_pre)
print('准确率为%.2f%%:'% (dt_evaluate_accuracy * 100.0))
dt_evaluate_p = precision_score(x_test['label'], model_dt_pre)
print('精确率为%.2f%%'% (dt_evaluate_p * 100.0))
# 绘制ROC曲线
tr_fpr, tr_tpr, tr_threasholds = roc_curve(x_test['label'], pre[:, 1])
plt.title("ROC %s(AUC=%.4f)"% ('曲线', auc))
plt.xlabel('假正率')
plt.ylabel('真正率')
plt.plot(tr_fpr, tr_tpr)
plt.show()


# 梯度提升分类
model = GradientBoostingClassifier(n_estimators=100, max_depth=5)
model.fit(x_train.drop(['label'], axis=1), x_train['label'])  # 模型训练
# 梯度提升评价指标
pre = model.predict_proba(x_test.drop(['label'], axis=1))  # 输出预测概率
auc = roc_auc_score(x_test['label'], pre[:, 1])  # 计算AUC值
print('AUC值为%.2f%%:'% (auc * 100.0))
pre1 = model.predict(x_test.drop(['label'], axis=1))
gb_evaluate_accuracy = accuracy_score(x_test['label'], pre1)
print('准确率为%.2f%%:'% (gb_evaluate_accuracy * 100.0))
gb_evaluate_p = precision_score(x_test['label'], pre1)
print('精确率为%.2f%%'% (gb_evaluate_p * 100.0))
# 绘制ROC曲线
tr_fpr, tr_tpr, tr_threasholds = roc_curve(x_test['label'], pre[:, 1])
plt.title("ROC %s(AUC=%.4f)"% ('曲线', auc))
plt.xlabel('假正率')
plt.ylabel('真正率')
plt.plot(tr_fpr, tr_tpr)
plt.show()


# XGBoost分类模型
model_xgb_evaluate = xgb.XGBClassifier(max_depth=6, learning_rate=0.1,
                                       n_estimators=150, silent=True, 
                                       objective='binary:logistic')
model_xgb_evaluate.fit(x_train.drop(['label'], axis=1), x_train['label'])

# 对验证样本进行预测
model_xgb_pre = model_xgb_evaluate.predict(x_test.drop(['label'], axis=1))

# XGBoost分类模型评价指标
pre = model_xgb_evaluate.predict_proba(x_test.drop(['label'], axis=1))  # 输出预测概率
auc = roc_auc_score(x_test['label'], pre[:, 1])  # 计算AUC值
print('AUC值为%.2f%%:'% (auc * 100.0))
xfb_evaluate_accuracy = accuracy_score(x_test['label'], model_xgb_pre)
print('准确率为:%.2f%%'% (xfb_evaluate_accuracy * 100.0))
xfb_evaluate_p = precision_score(x_test['label'], model_xgb_pre)
print('精确率为:%.2f%%'% (xfb_evaluate_p * 100.0))
# 绘制ROC曲线
tr_fpr, tr_tpr, tr_threasholds = roc_curve(x_test['label'], pre[:, 1])
plt.title("ROC %s(AUC=%.4f)"% ('曲线', auc))
plt.xlabel('假正率')
plt.ylabel('真正率')
plt.plot(tr_fpr, tr_tpr)
plt.show()

