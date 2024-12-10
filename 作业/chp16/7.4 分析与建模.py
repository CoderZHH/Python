# 构建Apriori模型实现菜品的关联分析
import pandas as pd
info = pd.read_csv('../tmp/info_clear.csv', encoding='utf-8')  # 读取处理后的订单表数据文件
detail = pd.read_csv('../tmp/detail_clear.csv', encoding='utf-8')  # 读取处理后的订单详情表数据文件

# 建立aliment列表，每个列表代表一个订单的菜品
order_id = detail[["order_id"]].drop_duplicates()
aliment = []
# 利用for循环获取订单菜品信息
for i in range(len(order_id)):
    dishes_name = detail['dishes_name'][detail.order_id==order_id.iloc[i][0]].tolist()
    aliment.append(dishes_name)

# 将aliment转为DataFrame并转置
from pandas.core.frame import DataFrame
aliment1 = DataFrame(aliment).T


# 构建Apriori模型的二元矩阵
dishes_name = detail["dishes_name"].drop_duplicates().tolist()
order_id = order_id.iloc[:,0].tolist()
# 创建新的数据框，index为order_id值，columns为dishes_name值
ruledata = pd.DataFrame(index=order_id, columns=dishes_name)
# 利用for循环获得购物篮二元矩阵
for i in range(len(order_id)):
    for j in range(len(dishes_name)):
        test_list = detail[(detail["order_id"]==order_id[i]) &
                           (detail["dishes_name"]==dishes_name[j])].index.tolist()
        if len(test_list) != 0:
            ruledata.iloc[i,j] = 1
        else:
            ruledata.iloc[i,j] = 0
# 写出数据
ruledata.to_csv('../tmp/ruledata.csv', header=1, index=1, encoding='utf-8_sig')


from apriori import * 
# 生成关联规则
support = 0.01
confidence = 0.5
ms = "---"
ruledata = pd.read_csv('../tmp/ruledata.csv', encoding='utf-8_sig', index_col=0)
rules = find_rule(ruledata,support,confidence,ms)
# 根据support进行排序
rules = rules.sort_values(by=['support'], axis=0, ascending=False)
# 保留3位小数
rules = rules.round(3)
# 写出生成的关联规则数据
rules.to_csv('../tmp/rules.csv', header=1, index=0, encoding='utf-8_sig')
