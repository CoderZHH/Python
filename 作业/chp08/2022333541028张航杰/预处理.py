import pandas as pd

# 读取所有列为字符串类型
data = pd.read_csv('./jc_content_viewlog1.csv', dtype=str)

# 数据筛选
seriesdata = data[['id', 'ip', 'date_time']]
# 去重
seiresdata = seriesdata.drop_duplicates(subset=['ip', 'date_time'])
seiresdata.to_csv('./seires.csv', index=False)
