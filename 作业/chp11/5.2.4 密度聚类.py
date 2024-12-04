from sklearn.cluster import DBSCAN
import sklearn.datasets as datasets
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 生成两簇非凸数据
x1, y2 = datasets.make_blobs(n_samples=1000, n_features=2,
                             centers=[[1, 1]], cluster_std=[[.1]],
                             random_state=9)
# 一簇对比数据
x2, y1 = datasets.make_circles(n_samples=2000, factor=.6, noise=.05)
x = np.concatenate((x1, x2))

# 生成DBSCAN模型
dbs = DBSCAN(eps=0.1, min_samples=12).fit(x)
print('DBSCAN模型:\n', dbs)

# 绘制DBSCAN模型聚类结果图
ds_pre = dbs.fit_predict(x)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(6, 6))
plt.scatter(x[:, 0], x[:, 1], c=ds_pre)
plt.title('密度聚类', size=17)
plt.show()

# 文档中的图形可以根据以下代码得出
from sklearn.cluster import DBSCAN
import sklearn.datasets as datasets
import matplotlib.pyplot as plt
import numpy as np

# 生成两簇非凸数据
x1, y2 = datasets.make_blobs(n_samples=1000, n_features=2,
                             centers=[[1, 1]], cluster_std=[[.1]],
                             random_state=9)
# 一簇对比数据
x2, y1 = datasets.make_circles(n_samples=2000, factor=.6, noise=.05)
x = np.concatenate((x1, x2))

# 生成DBSCAN模型
# 自动确定最优半径
from sklearn.neighbors import NearestNeighbors

# 计算 k-最近邻距离
neighbors = NearestNeighbors(n_neighbors=12)
neighbors_fit = neighbors.fit(x)
distances, indices = neighbors_fit.kneighbors(x)

# 对距离排序
distances = np.sort(distances, axis=0)
distances = distances[:, 1]
plt.plot(distances)
plt.title('k-最近邻距离图')
plt.xlabel('样本点')
plt.ylabel('距离')
plt.show()

# 根据图形选择最优半径
optimal_eps = distances[np.argmax(np.diff(distances))]
print('最优半径:', optimal_eps)

# 生成DBSCAN模型
dbs = DBSCAN(eps=optimal_eps, min_samples=12).fit(x)
print('DBSCAN模型:\n', dbs)
print('DBSCAN模型:\n', dbs)

# 绘制DBSCAN模型聚类结果图
ds_pre = dbs.fit_predict(x)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(6, 6))
plt.scatter(x[ds_pre == 0, 0], x[ds_pre == 0, 1])
plt.scatter(x[ds_pre == 1, 0], x[ds_pre == 1, 1])
plt.scatter(x[ds_pre == -1, 0], x[ds_pre == -1, 1], c='r', marker='^')
plt.title('密度聚类', size=17)
# plt.savefig('图5-15.jpg', dpi=1080)
plt.show()
