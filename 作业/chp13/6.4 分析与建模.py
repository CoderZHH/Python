import numpy as np
from sklearn.cluster import KMeans
import collections
from sklearn import metrics
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimHei'  # 正常显示中文

# 参数寻优
inertia = []
silhouettteScore = []
# 计算聚类数目为2至9时的轮廓系数值和簇内误差平方和
for i in range(2, 10):
    km = KMeans(n_clusters=i, random_state=12).fit(ScoreModel)
    y_pred = km.predict(ScoreModel)
    center_ = km.cluster_centers_
    score = metrics.silhouette_score(ScoreModel, km.labels_)
    silhouettteScore.append([i, score])
    inertia.append([i, km.inertia_])

# 绘制轮廓系数图
silhouettteScore = np.array(silhouettteScore)
plt.plot(silhouettteScore[: , 0], silhouettteScore[: , 1])
plt.title('轮廓系数值 - 聚类数目')
plt.show() 
#绘制簇内误差平方和图
inertia = np.array(inertia)
plt.plot(inertia[: , 0], inertia[: , 1])
plt.title('簇内误差平方和 - 聚类数目')
plt.show() 



# 构建K-Means聚类模型
KMeansModel = KMeans(n_clusters=4, random_state=12).fit(ScoreModel)
Cou = collections.Counter(KMeansModel.labels_)
print(Cou)
KMeansModel.cluster_centers_   # 查看中心点
center = KMeansModel.cluster_centers_
print(center)  # 聚类中心
names = ['历史信用风险', '经济风险情况', '收入风险情况']



# 绘制雷达图
fig = plt.figure(figsize=(10, 8.5))
ax = fig.add_subplot(111, polar=True)  # 定义polar参数为True，设置为极坐标格式
angles = np.linspace(0, 2 * np.pi, 3, endpoint=False)
angles = np.concatenate((angles, [angles[0]]))  # 闭合
Linecolor = ['bo-', 'r+:', 'gD--', 'kv-.']  # 点线颜色
Fillcolor = ['b', 'r', 'g', 'k']
# 设置每个标签的位置
plt.xticks(angles, names)
for label, i in zip(ax.get_xticklabels(), range(0,len(names))):
    if i < 1:
        angle_text = angles[i] * (-180 / np.pi) + 90
        label.set_horizontalalignment('left')
    else:
        angle_text = angles[i] * (-180 / np.pi) - 90
        label.set_horizontalalignment('right')
    label.set_rotation(angle_text)
# 绘制ylabels
ax.set_rlabel_position(0)
# 设置雷达图参数
for i in range(4):
    data = np.concatenate((center[i], [center[i][0]]))  # 闭合
    ax.plot(angles, data, Linecolor[i], linewidth=2)  # 画线
    ax.fill(angles, data, facecolor=Fillcolor[i], alpha=0.25)  # 填充颜色

ax.set_title('客户分群雷达图', va='bottom')  # 设定标题
ax.set_rlim(-2, 5)  # 设置各指标的最终范围
ax.grid(True)
plt.legend(['类别1', '类别2', '类别3', '类别4'])
plt.show()



