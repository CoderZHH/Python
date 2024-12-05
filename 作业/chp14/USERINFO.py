# 导入必要的库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA



# 设置绘图风格
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


def preprocess_data(file_path):
    """
    数据预处理函数：
    1. 读取数据
    2. 删除重复数据
    3. 删除指定列
    4. 确保每个客户信息一行
    5. 处理缺失值
    6. 处理异常值
    """
    # 读取数据
    data = pd.read_csv(file_path, encoding='gbk')
    print("原始数据形状:", data.shape)
    print("数据预览:\n", data.head())

    # 删除重复数据
    data = data.drop_duplicates()
    print("删除重复数据后的形状:", data.shape)

    # 删除手机品牌、手机型号和操作系统描述这3个属性
    columns_to_drop = ['MANU_NAME', 'MODEL_NAME', 'OS_DESC']
    data = data.drop(columns=columns_to_drop, errors='ignore')  # 使用errors='ignore'避免列不存在时报错
    print(f"删除列 {columns_to_drop} 后的数据形状:", data.shape)

    # 确保每个客户信息处理为一行数据
    # 假设USER_ID唯一标识每个客户
    aggregation_functions = {
        'MONTH_ID': 'first',
        'INNET_MONTH': 'max',
        'IS_AGREE': 'first',
        'AGREE_EXP_DATE': 'first',
        'CREDIT_LEVEL': 'max',
        'VIP_LVL': 'max',
        'ACCT_FEE': 'mean',
        'CALL_DURA': 'sum',
        'NO_ROAM_LOCAL_CALL_DURA': 'sum',
        'NO_ROAM_GN_LONG_CALL_DURA': 'sum',
        'GN_ROAM_CALL_DURA': 'sum',
        'CDR_NUM': 'sum',
        'NO_ROAM_CDR_NUM': 'sum',
        'NO_ROAM_LOCAL_CDR_NUM': 'sum',
        'NO_ROAM_GN_LONG_CDR_NUM': 'sum',
        'GN_ROAM_CDR_NUM': 'sum',
        'P2P_SMS_CNT_UP': 'sum',
        'TOTAL_FLUX': 'sum',
        'LOCAL_FLUX': 'sum',
        'GN_ROAM_FLUX': 'sum',
        'CALL_DAYS': 'max',
        'CALLING_DAYS': 'max',
        'CALLED_DAYS': 'max',
        'CALL_RING': 'sum',
        'CALLING_RING': 'sum',
        'CALLED_RING': 'sum',
        'CUST_SEX': 'first',
        'CERT_AGE': 'mean',
        'CONSTELLATION_DESC': 'first',
        'TERM_TYPE': 'first',
        'IS_LOST': 'max'
    }

    data = data.groupby('USER_ID').agg(aggregation_functions).reset_index()
    print("每个客户一行后的数据形状:", data.shape)

    # 处理缺失值
    print("缺失值情况:\n", data.isnull().sum())

    # 删除所有包含缺失值的行
    initial_shape = data.shape[0]
    data = data.dropna()
    final_shape = data.shape[0]
    print(f"删除包含缺失值的行: 删除了 {initial_shape - final_shape} 行")
    print("处理缺失值后的缺失情况:\n", data.isnull().sum())

    # 处理异常值
    def remove_outliers(df, column):
        """
        根据数据分布特点处理异常值：
        - 如果数据接近正态分布，使用Z分数方法。
        - 如果数据偏态较大，使用IQR方法。
        """
        skewness = df[column].skew()
        if abs(skewness) < 1:  # 偏度小于1，接近正态分布
            z_scores = np.abs(stats.zscore(df[column]))
            filtered_entries = z_scores < 3
            initial_shape = df.shape[0]
            df = df[filtered_entries]
            final_shape = df.shape[0]
            print(f"列 '{column}' 使用Z分数方法处理: 删除了 {initial_shape - final_shape} 行")
        else:  # 偏度较大，使用IQR方法
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            initial_shape = df.shape[0]
            df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
            final_shape = df.shape[0]
            print(f"列 '{column}' 使用IQR方法处理: 删除了 {initial_shape - final_shape} 行")
        return df
    # 识别数值型列
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()

    categorical_numeric_cols = ['CUST_SEX', 'IS_LOST', 'TERM_TYPE']
    numeric_cols = [col for col in numeric_cols if col not in categorical_numeric_cols ]

    # 删除异常值
    for col in numeric_cols:
        data = remove_outliers(data, col)

    print("删除异常值后的数据形状:", data.shape)

    return data


def analyze_customer_attributes(data):
    """
    客户属性分析：
    1. 性别分布
    2. 年龄分布
    3. 在网月份分布
    4. 合约到期时间分布
    5. 客户流失情况
    6. 信用等级分布
    7. 描述性统计
    """
    # 性别分析
    plt.figure(figsize=(6, 4))
    sns.countplot(x='CUST_SEX', data=data)
    plt.title('客户性别分布')
    plt.xlabel('性别（1: 男性, 2: 女性）')
    plt.ylabel('数量')
    plt.show()

    # 年龄分析
    plt.figure(figsize=(8, 6))
    sns.histplot(data['CERT_AGE'], bins=20, kde=True, color='skyblue')
    plt.title('客户年龄分布')
    plt.xlabel('年龄')
    plt.ylabel('数量')
    plt.show()

    # 在网月份分析
    plt.figure(figsize=(8, 6))
    sns.histplot(data['INNET_MONTH'], bins=20, kde=True, color='salmon')
    plt.title('客户在网月份分布')
    plt.xlabel('在网月数')
    plt.ylabel('数量')
    plt.show()

    # 合约到期时间分析
    plt.figure(figsize=(10, 6))
    sns.histplot(data['AGREE_EXP_DATE'], bins=20, kde=True, color='lightgreen')
    plt.title('合约到期时间分布')
    plt.xlabel('合约到期年月 (YYYYMM)')
    plt.ylabel('数量')
    plt.show()

    # 客户是否流失分析
    plt.figure(figsize=(6, 4))
    sns.countplot(x='IS_LOST', data=data)
    plt.title('客户流失情况')
    plt.xlabel('是否流失（1: 流失, 0: 未流失）')
    plt.ylabel('数量')
    plt.show()

    # 信用等级分析
    plt.figure(figsize=(8, 6))
    sns.histplot(data['CREDIT_LEVEL'], bins=20, kde=True, color='orchid')
    plt.title('客户信用等级分布')
    plt.xlabel('信用等级')
    plt.ylabel('数量')
    plt.show()

    # 描述性统计
    descriptive_stats = data[['CUST_SEX', 'CERT_AGE', 'INNET_MONTH',
                              'AGREE_EXP_DATE', 'CREDIT_LEVEL', 'IS_LOST']].describe()
    print("客户属性描述性统计:\n", descriptive_stats)


def perform_kmeans_clustering(data, n_clusters=5):
    """
    K-means聚类分析：
    1. 选择特征
    2. 标准化
    3. 训练K-means模型
    4. 模型评价（轮廓系数）
    5. 可视化聚类结果
    6. 查看各聚类特征中心
    """
    # 选择用于聚类的特征
    features = ['INNET_MONTH', 'CREDIT_LEVEL', 'VIP_LVL', 'ACCT_FEE',
                'CALL_DURA', 'GN_ROAM_CALL_DURA', 'CDR_NUM', 'TOTAL_FLUX',
                'CALL_DAYS', 'CALL_RING', 'CERT_AGE']

    # 检查所有特征是否存在于数据中
    missing_features = [feature for feature in features if feature not in data.columns]
    if missing_features:
        print(f"警告: 以下特征在数据中缺失: {missing_features}")
        features = [feature for feature in features if feature in data.columns]

    X = data[features]

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("特征标准化完成。")

    # 确定K值（这里使用用户指定的5）
    k = n_clusters
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    labels = kmeans.labels_
    print(f"K-means 聚类完成，聚类数量: {k}")

    # 将聚类标签添加到原数据中
    data['Cluster'] = labels

    # 模型评价
    silhouette_avg = silhouette_score(X_scaled, labels)
    print(f'K-means 聚类的轮廓系数 (Silhouette Score): {silhouette_avg:.4f}')

    # 可视化聚类结果（使用PCA降维至2维）
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    plt.figure(figsize=(10, 8))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=labels, palette='viridis', alpha=0.6)
    plt.title('K-means 聚类结果 (PCA降维)')
    plt.xlabel('主成分1')
    plt.ylabel('主成分2')
    plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

    # 各聚类的特征中心
    centers = kmeans.cluster_centers_
    centers_original = scaler.inverse_transform(centers)
    centers_df = pd.DataFrame(centers_original, columns=features)
    centers_df['Cluster'] = range(k)
    print("各聚类的特征中心 (逆标准化后):\n", centers_df)

    return data


def main():
    # 数据文件路径
    file_path = './USER_INFO_M.csv'  # 请确保文件路径正确

    # 数据预处理
    print("开始数据预处理...")
    data = preprocess_data(file_path)
    print("数据预处理完成。\n")

    # 客户属性分析
    print("开始客户属性分析...")
    analyze_customer_attributes(data)
    print("客户属性分析完成。\n")

    # K-means聚类分析
    print("开始K-means聚类分析...")
    data = perform_kmeans_clustering(data, n_clusters=5)
    print("K-means聚类分析完成。\n")

    # 保存处理后的数据（包括聚类标签）到新CSV文件
    output_file = './result.csv'
    data.to_csv(output_file, index=False)
    print(f"处理后的数据已保存到 '{output_file}'。")


if __name__ == "__main__":
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    main()
