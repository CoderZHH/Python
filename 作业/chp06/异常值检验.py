import numpy as np

# 定义数据数组
any = [19, 57, 68, 52, 79, 43, 55, 94, 376, 4581, 3648, 70, 51, 38]

# IQR准则对异常值进行检测
# 计算百分位数
Percentile = np.percentile(any, [0, 25, 50, 75, 100])
# 计算四分位距（IQR）
IQR = Percentile[3] - Percentile[1]
# 计算异常值的上界
UpLimit = Percentile[3] + IQR * 1.5
# 计算异常值的下界
arrayownLimit = Percentile[1] - IQR * 1.5

# 判断异常值，大于上界或小于下界的值即为异常值
abnormal = [i for i in any if i > UpLimit or i < arrayownLimit]
print('IQR准则检测出的异常值为：', abnormal)
print('IQR准则检测出的异常值比例为：', len(abnormal) / len(any))


# 计算平均值
array_mean = np.array(any).mean()
# 计算标准差
array_sarray = np.array(any).std()
# 计算每个元素与平均值的差值
array_cha = any - array_mean

# 返回异常值所在位置
ind = [i for i in range(len(array_cha)) if np.abs(array_cha[i]) > 3 * array_sarray]
# 根据位置返回异常值
abnormal = [any[i] for i in ind]
print('3sigma规则检测出的异常值为：', abnormal)
