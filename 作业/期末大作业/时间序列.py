import pandas as pd
import numpy as np

# 加载数据
matches_data = pd.read_excel("Wimbledon_featured_matches.xlsx")

# 将 elapsed_time 转换为字符串格式，再转换为 timedelta
matches_data['elapsed_time'] = matches_data['elapsed_time'].apply(lambda x: str(x).split(' ')[1] if ' ' in str(x) else str(x))
matches_data['elapsed_time'] = pd.to_timedelta(matches_data['elapsed_time'])

# 确保数据按时间和回合顺序排序
matches_data = matches_data.sort_values(by=['match_id', 'set_no', 'game_no', 'point_no'])

# 1. 累积跑动距离
matches_data['cumulative_distance_p1'] = matches_data.groupby('match_id')['p1_distance_run'].cumsum()
matches_data['cumulative_distance_p2'] = matches_data.groupby('match_id')['p2_distance_run'].cumsum()

# 2. 滑动窗口击球次数（窗口大小=5）
matches_data['rolling_rally_count'] = matches_data.groupby('match_id')['rally_count'].rolling(window=5, min_periods=1).mean().reset_index(level=0, drop=True)

# 3. 时间间隔特征
matches_data['time_diff'] = matches_data.groupby('match_id')['elapsed_time'].diff().dt.total_seconds().fillna(0)

# 查看引入的新特征
print(matches_data[['match_id', 'set_no', 'game_no', 'point_no',
                    'cumulative_distance_p1', 'cumulative_distance_p2',
                    'rolling_rally_count', 'time_diff']].head())

# 保存新的数据集
matches_data.to_excel("Wimbledon_with_time_features.xlsx", index=False)
