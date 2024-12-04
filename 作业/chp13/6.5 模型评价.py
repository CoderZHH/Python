import collections
import matplotlib.pyplot as plt

# 绘制不同客户类型客户数量饼图
TypeRate = collections.Counter(KMeansModel.labels_)
name_list = ['潜在高风险客户', '禁入类客户及高风险客户', '一般风险客户', '一般客户']
num_list = TypeRate.values()
print('查看各类客户数量:', num_list)
plt.figure(figsize=(8, 8))
# 绘制饼图
explode = [0, 0.1, 0, 0]  # 分离禁入类客户和高风险客户
plt.pie(num_list, labels=name_list, autopct='%1.1f%%', pctdistance=1.15, 
        explode=explode, labeldistance=1.05, startangle=90) 
plt.show()
