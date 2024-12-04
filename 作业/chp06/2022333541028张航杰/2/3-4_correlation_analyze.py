# 餐饮销量数据相关性分析
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 加载数据
catering_sale = './catering_sale_all.xls'  # 餐饮数据，含有其他属性
data = pd.read_excel(catering_sale, index_col='日期', header=0)  # 读取数据，指定“日期”列为索引列

# 打印数据确认读取成功
print(data)

# 相关性分析图
sns.set(font='SimHei', font_scale=1.5)  # 将 seaborn 字体设置为 SimHei，并调整字体大小
sns.pairplot(data, kind='reg', diag_kind='kde')
plt.show()