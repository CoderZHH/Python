from sklearn import datasets
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
# 导入数据
breast_cancer = datasets.load_breast_cancer()
x = breast_cancer.data
y = breast_cancer.target

# 层次聚类
clusing_ward = AgglomerativeClustering(n_clusters=3).fit(x)
print('层次聚类模型为：\n', clusing_ward)

# 绘制层次聚类结果图
cw_ypre = AgglomerativeClustering(n_clusters=3).fit_predict(x)
plt.scatter(x[:, 0], x[:, 1], c=cw_ypre)
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
plt.title('层次聚类', size=17)
plt.show()

#绘制树状图
from scipy.cluster import hierarchy
plt.figure(figsize=(5, 5))
Z = hierarchy.linkage(y=x, method='weighted', metric='euclidean')
hierarchy.dendrogram(Z, labels=cw_ypre)
plt.title('树状图', size=17)
plt.show()

from sklearn.metrics import fowlkes_mallows_score, adjusted_rand_score, davies_bouldin_score
print('层次聚类模型的FM系数：', fowlkes_mallows_score(y, cw_ypre))
print('层次聚类模型的调整Rand指数：', adjusted_rand_score(y, cw_ypre))
print('层次聚类模型的DB指数：', davies_bouldin_score(x, cw_ypre))
