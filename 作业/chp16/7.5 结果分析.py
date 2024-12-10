import pandas as pd
import numpy as np
sales_volume = pd.read_csv('../tmp/sales_volume.csv')
profit = pd.read_csv('../tmp/profit.csv')
dish = pd.read_csv('../data/meal_dishes_detail.csv')
rules = pd.read_csv('../tmp/rules.csv')
# 定义新列表
Lhs, Rhs = [], []
# 利用for循环将关联分析结果的前项和后项进行拆分，分别放置不同列中
for x in rules["rule"]:
    lhs = [x.replace("---",",")]
    lhs = lhs[0].split(",")
    length = len(lhs)
    rhs = lhs[length-1]
    lhs.pop(length-1)
    Lhs.append(str(lhs))
    Rhs.append(rhs)
rules["lhs"] = Lhs  # 前项
rules["rhs"] = Rhs  # 后项
# 删除rule列
rules_new = rules.drop(columns=["rule"])

# 统计前项
rules_count = rules_new.groupby(["lhs"])["lhs"].count()
# 计算每个菜所推荐的菜的综合评分
# 设A的权重a1 = 1.5, a2 = 2.5, a3 = 2, a4 = 4
A = np.mat(([0, 2.5, 2, 4],[1.5, 0, 2, 4],[1.5, 2.5, 0, 4],[1.5, 2.5, 2, 0]))
E = np.mat([1,1,1,1])
# 初始化
rules_new['sale'] = 0; rules_new['recommendation'] = 0; rules_new['profit'] = 0; rules_new['mark'] = 0

# 利用for循环找到对应菜品的热销度、毛利率和主推度，并计算综合得分
for i in range(rules_new.shape[0]):
    # 找到对应的热销度
    sales_num = sales_volume[sales_volume['dishes_name']==rules_new['rhs'].iloc[i]].index.tolist()
    rules_new['sale'].iloc[i] = float(sales_volume['sales_hot'].iloc[sales_num[0]])
     
    # 找到对应的毛利率和主推度
    profit_num = profit[profit['dishes_name']==rules_new['rhs'].iloc[i]].index.tolist()
    rules_new['profit'].iloc[i] = float(profit["rate"].iloc[profit_num[0]])
    rules_new['recommendation'].iloc[i] = float(profit['recommend_percent'].iloc[profit_num[0]])
    
    # 计算综合得分
    Y = np.mat([rules_new['sale'].iloc[i], rules_new['profit'].iloc[i], 
         rules_new['recommendation'].iloc[i], rules_new['support'].iloc[i]])
    rules_new['mark'].iloc[i] = round(float(np.dot(np.dot((E-Y),A),Y.T)),3)

# 对综合得分排序
rules_new = rules_new.sort_values(by=['mark'], axis=0, ascending=False)
rules['support'].round(3)
rules_new.to_csv('../tmp/recommend.csv', encoding='utf-8_sig', header=1)
# 选取后项为“芹菜炒腰花”的数据
rules_item = rules_new[rules_new['rhs']=='芹菜炒腰花']
rules_item['support'].round(3)
rules_item = rules_item[['lhs', 'rhs', 'support', 'confidence', 'sale', 'recommendation',
               'profit', 'mark']]
rules_item.to_csv('../tmp/rules_item.csv', encoding='utf-8_sig', header=1)

