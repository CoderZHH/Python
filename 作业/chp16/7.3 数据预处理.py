import pandas as pd
dish = pd.read_csv('../data/meal_dishes_detail.csv', encoding='utf-8')
detail = pd.read_csv('../tmp/detail.csv', encoding='utf-8')
info = pd.read_csv('../tmp/info.csv', encoding='utf-8')

# 删除白饭的记录
drop_index = detail[(detail.dishes_name=='白饭/小碗') |
        (detail.dishes_name=='白饭/大碗')].index.tolist()
detail = detail.drop(drop_index)

# 筛选属性
info_1_ = info[['info_id', 'emp_id', 'number_consumers', 'expenditure',
                  'dishes_count', 'accounts_payable', 'use_start_time', 
                  'lock_time', 'order_status', 'phone', 'name']]
detail = detail[['detail_id', 'order_id', 'dishes_id', 'dishes_name', 
                 'counts', 'amounts', 'place_order_time', 'emp_id']]

# 写出处理后的订单表和订单详情表
info_1_.to_csv('../tmp/info_clear.csv', index=0, header=1, encoding='utf-8_sig')
detail.to_csv('../tmp/detail_clear.csv', index=0, header=1, encoding='utf-8_sig')


# 删除菜品名称的回车符和换行符
dish['dishes_name'] = dish['dishes_name'].apply(lambda x:
    x.replace(' ', '').replace('\n', '').replace('\r', ''))
    
# 筛选属性计算毛利率
profit = dish[['id', 'dishes_name', 'price', 'cost', 'recommend_percent']]
profit['rate'] = 0
dish.head()
profit.head()
for i in range(profit.shape[0]):
    profit['rate'].iloc[i] = round((profit["price"].iloc[i]-profit["cost"].iloc[i])
    /profit["price"].iloc[i],2)
# 写出毛利率数据
profit.to_csv('../tmp/profit.csv', encoding='utf-8_sig')


