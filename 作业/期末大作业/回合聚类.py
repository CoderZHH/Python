import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from mpl_toolkits.mplot3d import Axes3D

# 支持中文显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号不能显示的问题

# Step 1: 加载数据
matches_path = './Wimbledon_featured_matches.xlsx'
matches_data = pd.read_excel(matches_path)

# Step 2: 选择回合级别的原始特征
round_cols = ['set_no', 'game_no', 'point_no', 'rally_count', 'speed_mph',
              'p1_distance_run', 'p2_distance_run', 'p1_ace', 'p2_ace',
              'p1_unf_err', 'p2_unf_err']
round_stats = matches_data[round_cols].copy()

# Step 3: 补充缺失值进行处理：分组均值补充 + 全局均值补充
round_stats['speed_mph'] = round_stats.groupby(['set_no', 'game_no', 'point_no'])['speed_mph'].transform(lambda x: x.fillna(x.mean()))
round_stats['speed_mph'] = round_stats['speed_mph'].fillna(round_stats['speed_mph'].mean())

# Step 4: 创建回合级别的特征工程
# 每击球的平均跑动距离
round_stats['average_distance_per_rally'] = (round_stats['p1_distance_run'] + round_stats['p2_distance_run']) / (round_stats['rally_count'] + 1)

# 跑动距离差异
round_stats['distance_diff'] = abs(round_stats['p1_distance_run'] - round_stats['p2_distance_run'])

# ACE效率
round_stats['ace_efficiency'] = (round_stats['p1_ace'] + round_stats['p2_ace']) / (round_stats['rally_count'] + 1)

# 改进 is_key_point 的定义
round_stats['is_key_point'] = ((round_stats['p1_ace'] > 0) | (round_stats['p2_ace'] > 0) |
                               (round_stats['p1_unf_err'] > 0) | (round_stats['p2_unf_err'] > 0) |
                               (round_stats['rally_count'] > 10)).astype(int)

# 改进 unf_err_to_ace_ratio 的逻辑，避免分母为零
round_stats['unf_err_to_ace_ratio'] = (round_stats['p1_unf_err'] + round_stats['p2_unf_err']) / (
    round_stats['p1_ace'] + round_stats['p2_ace'] + 1)

# Step 5: 选择用于聚类的特征
features_for_clustering = round_stats[['rally_count', 'speed_mph', 'average_distance_per_rally',
                                        'distance_diff', 'ace_efficiency', 'unf_err_to_ace_ratio','is_key_point']]

# Step 6: 特征标准化
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_for_clustering)

# Step 7: 使用肘部法则确定最佳簇数
inertia = []
cluster_range = range(2, 10)
for k in cluster_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(features_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(cluster_range, inertia, marker='o', linestyle='--')
plt.xlabel('簇的数量', fontsize=12)
plt.ylabel('簇内误差平方和 (Inertia)', fontsize=12)
plt.title('肘部法则确定最佳簇数量', fontsize=14)
plt.show()

# Step 8: 应用KMeans进行聚类
optimal_clusters = 3  # 可根据肘部图调整
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
round_stats['Cluster'] = kmeans.fit_predict(features_scaled)

# Step 9: 聚类性能评估
silhouette_avg = silhouette_score(features_scaled, kmeans.labels_)
davies_bouldin = davies_bouldin_score(features_scaled, kmeans.labels_)
print(f"轮廓系数 (Silhouette Score): {silhouette_avg:.4f}")
print(f"戴维森堡丁指数 (Davies-Bouldin Index): {davies_bouldin:.4f}")

# Step 10: PCA降维与聚类结果可视化
pca = PCA(n_components=3)
features_pca = pca.fit_transform(features_scaled)
round_stats['PCA1'] = features_pca[:, 0]
round_stats['PCA2'] = features_pca[:, 1]
round_stats['PCA3'] = features_pca[:, 2]

# 2D 可视化
plt.figure(figsize=(10, 6))
for cluster in range(optimal_clusters):
    cluster_data = round_stats[round_stats['Cluster'] == cluster]
    plt.scatter(cluster_data['PCA1'], cluster_data['PCA2'], label=f'簇 {cluster}', alpha=0.7)
plt.xlabel('PCA 组件 1', fontsize=12)
plt.ylabel('PCA 组件 2', fontsize=12)
plt.title('回合表现聚类结果 (2D 可视化)', fontsize=14)
plt.legend()
plt.show()

# 3D 可视化
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
for cluster in range(optimal_clusters):
    cluster_data = round_stats[round_stats['Cluster'] == cluster]
    ax.scatter(cluster_data['PCA1'], cluster_data['PCA2'], cluster_data['PCA3'], label=f'簇 {cluster}', alpha=0.7)
ax.set_xlabel('PCA 组件 1', fontsize=10)
ax.set_ylabel('PCA 组件 2', fontsize=10)
ax.set_zlabel('PCA 组件 3', fontsize=10)
ax.set_title('回合表现聚类结果 (3D 可视化)', fontsize=12)
plt.legend()
plt.show()


# 计算每个簇的特征均值
cluster_summary = round_stats.groupby('Cluster')[features_for_clustering.columns].mean()
cluster_summary.to_excel('./回合聚类结果.xlsx', index=True)