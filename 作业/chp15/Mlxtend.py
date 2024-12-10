from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# 读取数据
user_goods = pd.read_excel('goods_new.xls', header=None)

# 数据预处理为0-1矩阵
ct = lambda x: pd.Series(1, index=x[pd.notnull(x)])
b = map(ct, user_goods.values)
data = pd.DataFrame(list(b)).fillna(0).astype(int)

# 将数据转换为布尔类型
data = data.astype(bool)

# Apriori算法
frequent_itemsets = apriori(data, min_support=0.2, use_colnames=True)

# 关联规则分析
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5, num_itemsets=len(frequent_itemsets))

# 输出结果
rules.to_excel('apriori_rules.xlsx', index=False)
print("Apriori规则分析结果已保存为 'apriori_rules.xlsx'")

# 1. 散点图: 支持度 vs 置信度，颜色表示提升度
plt.figure(figsize=(10, 6))
plt.scatter(rules['support'], rules['confidence'], c=rules['lift'], cmap='viridis', s=100)
plt.colorbar(label='Lift')
plt.xlabel('Support')
plt.ylabel('Confidence')
plt.title('Support vs Confidence (Color: Lift)')
plt.grid(True)
plt.show()

# 2. 频繁项集支持度柱状图
top_items = frequent_itemsets.nlargest(10, 'support')
plt.figure(figsize=(10, 6))
plt.barh(top_items['itemsets'].astype(str), top_items['support'], color='skyblue')
plt.xlabel('Support')
plt.ylabel('Itemsets')
plt.title('Top 10 Frequent Itemsets')
plt.gca().invert_yaxis()
plt.show()

# 3. 关联规则热力图 (基于提升度)
pivot = rules.pivot(index='antecedents', columns='consequents', values='lift')
pivot.fillna(0, inplace=True)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True)
plt.title('Heatmap of Lift between Antecedents and Consequents')
plt.show()

# 4. 规则网络图 (展示前10个关联规则)
G = nx.DiGraph()

# 添加节点和边
for _, row in rules.head(10).iterrows():
    for antecedent in row['antecedents']:
        for consequent in row['consequents']:
            G.add_edge(antecedent, consequent, weight=row['lift'])

# 绘制网络图
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5)
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')
plt.title('Top 10 Association Rules Network Graph')
plt.axis('off')
plt.show()