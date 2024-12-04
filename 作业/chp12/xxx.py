import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. 读取数据
data = pd.read_csv("./user_info_screen.csv",encoding='gbk')

# 2. 分割数据集为特征（X）和目标变量（y）
X = data.drop(columns=['IS_LOST', 'USER_ID', 'AGREE_EXP_DATE'])  # 删除不相关的列
y = data['IS_LOST']

# 3. 分割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 数值特征和类别特征区分
numerical_features = ['CREDIT_LEVEL', 'VIP_LVL', 'ACCT_FEE', 'CALL_DURA', 'NO_ROAM_LOCAL_CALL_DURA',
                      'NO_ROAM_GN_LONG_CALL_DURA', 'GN_ROAM_CALL_DURA', 'CDR_NUM', 'NO_ROAM_CDR_NUM',
                      'NO_ROAM_LOCAL_CDR_NUM', 'NO_ROAM_GN_LONG_CDR_NUM', 'GN_ROAM_CDR_NUM', 'P2P_SMS_CNT_UP',
                      'TOTAL_FLUX', 'LOCAL_FLUX', 'GN_ROAM_FLUX', 'CALL_DAYS', 'CALLING_DAYS', 'CALLED_DAYS',
                      'CALL_RING', 'CALLING_RING', 'CALLED_RING', 'CERT_AGE', 'TERM_TYPE']

categorical_features = ['IS_AGREE', 'INNET_MONTH', 'CUST_SEX', 'CONSTELLATION_DESC', 'MANU_NAME', 'MODEL_NAME', 'OS_DESC']

# 5. 数值特征预处理
# 使用SimpleImputer处理缺失值，并使用StandardScaler进行标准化
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # 用均值填充缺失值
    ('scaler', StandardScaler())  # 标准化数据
])

# 6. 类别特征预处理
# 使用SimpleImputer填补缺失值，使用OneHotEncoder进行独热编码
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # 用最频繁值填充缺失值
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  # 独热编码
])

# 7. 使用ColumnTransformer来将预处理应用到不同的列
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# 8. 创建模型并加入预处理步骤
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))  # 使用随机森林作为分类器
])

# 9. 训练模型
model.fit(X_train, y_train)

# 10. 预测
y_pred = model.predict(X_test)

# 11. 输出模型评估
accuracy = accuracy_score(y_test, y_pred)
print(f"模型准确率: {accuracy}")

# 混淆矩阵
conf_matrix = confusion_matrix(y_test, y_pred)
print("混淆矩阵:")
print(conf_matrix)

# 分类报告
class_report = classification_report(y_test, y_pred)
print("分类报告:")
print(class_report)
