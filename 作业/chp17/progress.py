import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt
import networkx as nx
import mlxtend
import matplotlib.gridspec as gridspec

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 1. 数据加载与清洗
def load_and_clean_data(file_path):
    """
    加载CSV数据并进行清洗处理。

    参数:
        file_path (str): 数据文件的路径。

    返回:
        pd.DataFrame: 清洗后的数据框。
    """
    try:
        # 读取数据
        data = pd.read_csv(file_path, encoding='utf-8')  # 根据文件编码调整
        print("数据加载成功。")
    except Exception as e:
        print(f"读取数据失败: {e}")
        return None

    # 查看基本信息
    print("数据基本信息:")
    print(data.info())

    # 去除缺失关键字段的记录
    data_cleaned = data.dropna(subset=['ip', 'page_path'])
    print(f"去除缺失值后，数据量: {data_cleaned.shape[0]}")

    return data_cleaned


# 2. 提取用户浏览的网址
def extract_user_transactions(data):
    """
    根据唯一IP提取用户访问的所有网址。

    参数:
        data (pd.DataFrame): 清洗后的数据框。

    返回:
        list of list: 每个子列表包含一个用户访问的所有网址。
    """
    # 确保IP唯一性：将同一IP的所有访问视为一个用户的交易
    user_transactions = data.groupby('ip')['page_path'].apply(list).tolist()
    print(f"提取到的用户交易数量: {len(user_transactions)}")
    return user_transactions


# 3. 应用Apriori算法挖掘关联规则
def apply_apriori(transactions, min_support=0.01, min_confidence=0.5, min_lift=1.0):
    """
    使用Apriori算法挖掘频繁项集和关联规则。

    参数:
        transactions (list of list): 用户交易数据。
        min_support (float): 最小支持度。
        min_confidence (float): 最小置信度。
        min_lift (float): 最小提升度。

    返回:
        pd.DataFrame: 关联规则数据框。
    """
    # 独热编码
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    print("独热编码完成。")

    # 挖掘频繁项集
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    print(f"发现的频繁项集数量: {frequent_itemsets.shape[0]}")

    # 生成关联规则

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence, num_itemsets=100)
    print(f"生成的关联规则数量: {rules.shape[0]}")

    # 过滤提升度
    rules = rules[rules['lift'] >= min_lift]
    print(f"筛选后的关联规则数量 (lift >= {min_lift}): {rules.shape[0]}")

    return rules


# 4. 分析和输出关联规则
def analyze_rules(rules, top_n=10):
    """
    分析并输出关联规则。

    参数:
        rules (pd.DataFrame): 关联规则数据框。
        top_n (int): 要输出的前N条规则。
    """
    # 按置信度排序
    rules_sorted = rules.sort_values(by='confidence', ascending=False)

    print(f"\nTop {top_n} 关联规则（按置信度排序）:")
    for i, row in rules_sorted.head(top_n).iterrows():
        antecedents = ', '.join(list(row['antecedents']))
        consequents = ', '.join(list(row['consequents']))
        support = row['support']
        confidence = row['confidence']
        lift = row['lift']
        print(
            f"规则 {i + 1}: {antecedents} => {consequents} (支持度: {support:.4f}, 置信度: {confidence:.4f}, 提升度: {lift:.4f})")


# 5. 可视化关联规则（可选）
def visualize_rules(rules, lift_threshold=1.2, top_n=100):
    """
    可视化关联规则，展示提升度高于阈值的规则，并限制可视化的规则数量。

    参数:
        rules (pd.DataFrame): 关联规则数据框。
        lift_threshold (float): 提升度阈值。
        top_n (int): 要可视化的规则数量。
    """
    # 选择提升度较高的规则
    rules_high_lift = rules[rules['lift'] > lift_threshold]
    print(f"提升度大于 {lift_threshold} 的规则数量: {rules_high_lift.shape[0]}")

    if rules_high_lift.empty:
        print("没有满足提升度阈值的规则可视化。")
        return

    # 按照提升度排序并选择前 top_n 条规则
    rules_high_lift = rules_high_lift.sort_values(by='lift', ascending=False).head(top_n)
    print(f"可视化前 {top_n} 条提升度最高的规则。")

    # 创建网络图
    G = nx.DiGraph()

    for _, row in rules_high_lift.iterrows():
        antecedents = list(row['antecedents'])
        consequents = list(row['consequents'])
        for a in antecedents:
            for c in consequents:
                G.add_edge(a, c, weight=row['lift'])

    # 使用 GridSpec 创建布局
    fig = plt.figure(figsize=(20, 15))
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])

    # 绘制网络图
    ax1 = plt.subplot(gs[0])
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    edges = G.edges(data=True)
    weights = [edge[2]['weight'] for edge in edges]

    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue', ax=ax1)

    # 绘制边
    nx.draw_networkx_edges(
        G, pos, edgelist=edges, arrowstyle='->',
        arrowsize=20, edge_color=weights, edge_cmap=plt.cm.Blues,
        width=2, ax=ax1
    )

    # 绘制标签
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', ax=ax1)

    ax1.set_title(f'网址关联规则网络图 (前 {top_n} 条提升度最高的规则)')
    ax1.axis('off')

    # 创建颜色条轴
    ax2 = plt.subplot(gs[1])
    sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(vmin=min(weights), vmax=max(weights)))
    sm.set_array([])
    plt.colorbar(sm, cax=ax2, label='提升度')

    plt.tight_layout()
    plt.show()


# 主函数
def main():
    file_path = 'jc_content_viewlog.csv'

    # 1. 加载并清洗数据
    data_cleaned = load_and_clean_data(file_path)
    if data_cleaned is None:
        return

    # 2. 提取用户交易
    transactions = extract_user_transactions(data_cleaned)

    # 3. 应用Apriori算法
    rules = apply_apriori(transactions, min_support=0.01, min_confidence=0.5, min_lift=1.0)

    if rules.empty:
        print("未发现满足条件的关联规则。")
        return

    # 4. 分析和输出关联规则
    analyze_rules(rules, top_n=10)

    # 5. 可视化关联规则（可选）
    visualize = input("\n是否需要可视化关联规则？（y/n）: ").strip().lower()
    if visualize == 'y':
        visualize_rules(rules, lift_threshold=1.2, top_n=100)


if __name__ == "__main__":
    main()
