import pandas as pd
import graphviz
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.metrics import accuracy_score
from sklearn.tree import export_graphviz

# 读取数据
sales_data = pd.read_excel('./sales_data.xls', index_col='id')

# 数据预处理
sales_data[sales_data == '好'] = 1
sales_data[sales_data == '是'] = 1
sales_data[sales_data == '高'] = 1
sales_data[sales_data != 1] = -1

x = sales_data.iloc[:, :3].astype(int)
y = sales_data.iloc[:, 3].astype(int)

# 数据集拆分
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 创建决策树模型
dtc = DTC(criterion='entropy')
dtc.fit(x_train, y_train)

# 计算准确率
y_pred = dtc.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'模型准确度：{accuracy:.2f}')

# 导出决策树
dot_file_path = './tree.dot'

# 导出决策树为.dot文件
with open(dot_file_path, 'w', encoding='utf-8') as f:
    export_graphviz(
        dtc,
        feature_names=x.columns,
        class_names=['bad', 'good'],  # 添加中文类名
        filled=True,
        rounded=True,
        special_characters=True,  # 允许特殊字符
        out_file=f
    )

# 打开 .dot 文件并修改字体为支持中文的字体
with open(dot_file_path, 'r', encoding='utf-8') as f:
    dot_content = f.read()

# 替换字体为支持中文的字体
dot_content = dot_content.replace('node [', 'node [fontname="Microsoft YaHei", ')
dot_content = dot_content.replace('edge [', 'edge [fontname="Microsoft YaHei", ')

# 保存修改后的 .dot 文件
with open(dot_file_path, 'w', encoding='utf-8') as f:
    f.write(dot_content)

# 渲染决策树为图像并展示
graph = graphviz.Source(dot_content)
output_path = './tree'  # 输出路径
graph.render(output_path, view=True, format='pdf')  # 渲染为PDF格式并打开
