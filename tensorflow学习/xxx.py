import matplotlib.pyplot as plt
import numpy as np

# 定义一个函数来绘制值数组
def plot_value_array(values, true_index=None):
    plt.grid(False)  # 不显示网格线
    plt.xticks(range(len(values)))  # 将x轴刻度设置为数组索引
    plt.yticks([])  # 不显示y轴刻度
    plt.bar(range(len(values)), values, color="#777777")  # 绘制条形图

    # 如果提供了真实值的索引，突出显示该值
    if true_index is not None:
        plt.bar(true_index, values[true_index], color='red')

# 示例使用
values = np.random.rand(10)  # 一个随机生成的值数组（例如，预测值）
true_value_index = np.argmax(values)  # 假设真实值是值最大的那个

plt.figure(figsize=(6,3))
plot_value_array(values, true_value_index)
plt.show()
