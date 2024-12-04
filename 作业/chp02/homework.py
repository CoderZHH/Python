import pandas as pd

# 1. 读取CSV文件，注意处理中文
df = pd.read_csv('sc.csv', encoding='gbk')

# 1. 提取医生的唯一编码
unique_doctors = df['doctor_url'].unique()
print('1.', unique_doctors)

# 2. 提取回复时间下的日期，形成单独一列
df['answer_date'] = pd.to_datetime(df['answer_time'].str.strip("[]'"), format='%Y-%m-%d %H:%M:%S')
print('2.', df['answer_date'])

# 3. 计算回复时间和提问时间的时间差（按照秒算），形成单独一列
df['answer_time'] = pd.to_datetime(df['answer_time'].str.strip("[]'"), format='%Y-%m-%d %H:%M:%S')
df['question_time'] = pd.to_datetime(df['question_time'])
df['time_difference'] = (df['answer_time'] - df['question_time']).dt.total_seconds()
print('3.', df['time_difference'])

# 4. 提取患者年龄，形成单独一列
df['new_patient_age'] = df['patient_age'].str.extract('(\d+)')[0].astype(int)
print('4.', df['new_patient_age'])

# 5. 提取悬赏金额，形成单独一列
df['reward_amount'] = df['reward'].str.extract('(\d+)')[0].astype(float)
print('5.', df['reward_amount'])

# 6. 统计每位医生回复的患者人数
doctor_patient_count = df.groupby('doctor_url')['patient_sex'].count().reset_index(name='patient_count')
print('6.', doctor_patient_count)

# 7. 统计每位医生每天回复的患者人数
doctor_daily_count = df.groupby(['doctor_url', 'answer_date'])['patient_sex'].count().reset_index(name='daily_patient_count')
print('7.', doctor_daily_count)

# 保存处理后的 DataFrame 到 CSV 文件
df.to_csv('processed_sc.csv', index=False, encoding='utf-8-sig')
