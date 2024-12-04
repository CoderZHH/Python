import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

# 设置 Matplotlib 参数支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
plt.rcParams['axes.unicode_minus'] = False  # 负号显示

# 读取数据
file_path = './seires.csv'
data = pd.read_csv(file_path)
data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')

# 聚合数据按日期统计访问量
data['date'] = data['date_time'].dt.date
daily_visits = data.groupby('date').size().reset_index(name='visits')

# 设置时间序列索引
daily_visits['date'] = pd.to_datetime(daily_visits['date'])
daily_visits.set_index('date', inplace=True)

# 填补缺失日期，填充缺失值为0
daily_visits = daily_visits.asfreq('D', fill_value=0)

# 绘制原始时间序列
plt.figure(figsize=(10, 6))
plt.plot(daily_visits['visits'], label='每日访问量')
plt.title('每日访问量趋势')
plt.xlabel('日期')
plt.ylabel('访问量')
plt.legend()
plt.savefig('./img/每日访问量趋势.png')
plt.show()


# 检验数据平稳性并确定差分次数（d）
def test_stationarity(series, max_diff=5):
    d = 0
    while d < max_diff:
        adf_test = adfuller(series.dropna())
        p_value = adf_test[1]
        print(f"ADF检验 p-value: {p_value}")
        if p_value > 0.05:
            print(f"数据非平稳，进行第 {d + 1} 次差分处理")
            series = series.diff().dropna()
            d += 1
        else:
            print("数据已平稳")
            return series, d
    raise ValueError(f"数据在最大差分次数 {max_diff} 次后仍未平稳，请检查数据或采用其他方法处理。")


# 对时间序列进行平稳性检验并差分
daily_visits['visits_diff'], d = test_stationarity(daily_visits['visits'])

# 绘制差分后的时间序列
plt.figure(figsize=(10, 6))
plt.plot(daily_visits['visits_diff'], label='差分后的访问量')
plt.title('差分后的每日访问量')
plt.xlabel('日期')
plt.ylabel('访问量')
plt.legend()
plt.savefig('./img/差分后的每日访问量.png')
plt.show()

# 自相关图与偏自相关图
fig, ax = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(daily_visits['visits_diff'].dropna(), ax=ax[0], title='自相关图')
plot_pacf(daily_visits['visits_diff'].dropna(), ax=ax[1], title='偏自相关图')
plt.savefig('./img/自相关与偏自相关图.png')
plt.show()

# 白噪声检验
lb_test = acorr_ljungbox(daily_visits['visits_diff'].dropna(), lags=[10])
print(f"Ljung-Box检验 p-value: {lb_test['lb_pvalue'].values[0]}")

# 使用BIC准则定阶
bic_values = []
max_p = 5  # 限制最大阶数
max_q = 5
for p in range(max_p):
    for q in range(max_q):
        try:
            model = ARIMA(daily_visits['visits'], order=(p, d, q)).fit()
            bic_values.append((p, q, model.bic))
        except Exception as e:
            print(f"模型阶数 p={p}, q={q} 拟合失败: {e}")
            continue
best_p, best_q = min(bic_values, key=lambda x: x[2])[:2]
print(f"最佳阶数 p, q: {best_p}, {best_q}")

# 使用最佳阶数训练模型
model = ARIMA(daily_visits['visits'], order=(best_p, d, best_q))
model_fit = model.fit()
print(model_fit.summary())

# 预测未来7天访问量
forecast = model_fit.forecast(steps=7)
forecast_dates = pd.date_range(daily_visits.index[-1] + pd.Timedelta(days=1), periods=7)
forecast_series = pd.Series(forecast, index=forecast_dates)

# 绘制预测结果
plt.figure(figsize=(10, 6))
plt.plot(daily_visits['visits'], label='历史访问量')
plt.plot(forecast_series.index, forecast_series, label='预测访问量', linestyle='--', color='red')
plt.title('未来7天访问量预测')
plt.xlabel('日期')
plt.ylabel('访问量')
plt.legend()
plt.savefig('./img/未来7天访问量预测.png')
plt.show()

# 保存预测结果
forecast_series.to_csv('./预测结果.csv', header=True, encoding='utf-8-sig')

print("预测完成，预测结果已保存为 预测结果.csv")
