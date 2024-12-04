import json
import pandas as pd
import numpy as np

# 加载 JSON 文件
with open('./results.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 将 JSON 转换为 DataFrame
df = pd.json_normalize(data)

# 添加顺序索引编码（为每个条目增加一个序号）
df['index'] = np.arange(len(df))

# 随机抽取 10% 的数据
sampled_df = df.sample(frac=0.1, random_state=42)

# 将抽取的样本保存为 JSON 文件
sampled_df.to_json('./sampled_results.json', orient='records', force_ascii=False)

sampled_df.to_excel('./sampled_results.xlsx')