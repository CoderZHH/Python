import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
from radar_map import plot

# 导入数据并标准化
features = pd.read_excel('air_features.xlsx', index_col='ID')
features_scaler = (features - features.mean()) / features.std()

# 开始K-Means聚类
model = KMeans(n_clusters=5, random_state=3)
model.fit(features_scaler)
labs = model.labels_
centers = model.cluster_centers_

# 简单打印结果
r1 = pd.Series(model.labels_).value_counts()
r2 = pd.DataFrame(model.cluster_centers_)
r = pd.concat([r2, r1], axis=1)
r.columns = list(features.columns) + ['类别数目']
print(r)

# 详细输出原始数据及对应的类别
r = pd.concat([features, pd.Series(model.labels_, index=features.index)], axis=1)
r.columns = list(features.columns) + ['聚类类别']
r.to_excel('features_type.xlsx')


# 可视化雷达图
def plot_kmeans_radar(kmeans_model, columns):
    # 计算雷达图的角度
    angles = np.linspace(0, 2 * np.pi, len(columns), endpoint=False).tolist()
    angles += angles[:1]  # 闭合雷达图

    # 特征标签
    feature = columns.tolist()
    feature += feature[:1]  # 闭合雷达图

    # 绘图
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # 获取聚类中心数据
    cluster_centers = kmeans_model.cluster_centers_

    for i, center in enumerate(cluster_centers):
        ax.plot(angles, center.tolist() + [center[0]], label=f'Cluster {i + 1}')

    ax.set_thetagrids(np.degrees(angles), feature)
    ax.set_title("K-Means Clustering Radar Plot")
    ax.legend()
    plt.show()


# 调用雷达图函数
plot_kmeans_radar(kmeans_model=model, columns=features.columns)

# PCA 降维并绘制聚类散点图
pca = PCA(n_components=2)
pca.fit(features_scaler)
data_pca = pca.transform(features_scaler)
data_pca = pd.DataFrame(data_pca, columns=['PC1', 'PC2'])
data_pca['labels'] = labs

# 聚类中心降维
pca.fit(centers)
data_pca_centers = pca.transform(centers)
data_pca_centers = pd.DataFrame(data_pca_centers, columns=['PC1', 'PC2'])

# 可视化聚类结果
plt.figure(figsize=(8, 6))
plt.scatter(data_pca['PC1'], data_pca['PC2'], s=3, c=data_pca['labels'], cmap='Accent')
plt.scatter(data_pca_centers['PC1'], data_pca_centers['PC2'], marker='o', s=55, c='#8E00FF')
plt.show()
#
# # 使用 t-SNE 降维
# tsne = TSNE()
# tsne_results = tsne.fit_transform(features_scaler)
# tsne = pd.DataFrame(tsne_results, index=features_scaler.index)
#
# # 可视化 t-SNE
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# for label in range(5):
#     d = tsne[r['聚类类别'] == label]
#     plt.plot(d[0], d[1], label=f'class{label}')
# plt.legend()
# plt.show()

# 3D 可视化
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
pca = PCA(n_components=3)
pca.fit(features_scaler)
X = pca.transform(features_scaler)
xs, ys, zs = X[:, 0], X[:, 1], X[:, 2]
L = labs

# 聚类标签显示
for name, label in [('class1', 0), ('class2', 1), ('class3', 2), ('class4', 3), ('class5', 4)]:
    ax.text3D(X[L == label, 0].mean(), X[L == label, 1].mean() + 1.5, X[L == label, 2].mean(), name,
              horizontalalignment='center', bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))

# 绘制3D散点
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=L, cmap=plt.cm.nipy_spectral, edgecolor='k')

ax.set_xlim(min(xs), max(xs))
ax.set_ylim(min(ys), max(ys))
ax.set_zlim(min(zs), max(zs))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
plt.show()
