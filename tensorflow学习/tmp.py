# 导入 TensorFlow 和 Keras 层，用于构建神经网络
import tensorflow as tf

print("TensorFlow version:", tf.__version__)

# 从 Keras 导入常用的层
from keras.layers import Dense, Flatten, Conv2D
from keras import Model

# 加载 MNIST 数据集，它包含手写的数字（0-9）
mnist = tf.keras.datasets.mnist

# 将数据集分为训练集和测试集
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 将像素值从 [0, 255] 归一化到 [0.0, 1.0]，以便加快模型收敛
x_train, x_test = x_train / 255.0, x_test / 255.0

# 添加通道维度，使数据与 Conv2D 层兼容
x_train = x_train[..., tf.newaxis].astype("float32")
x_test = x_test[..., tf.newaxis].astype("float32")

# 使用 TensorFlow 的 tf.data API 将数据集切分为批次，并混合数据集
# shuffle(10000) 先将数据集随机打乱，使每个样本在训练时都能够随机选择，避免有序性带来的潜在偏差。
# batch(2) 然后将打乱后的数据集分成大小为 2 的小批次，模型会一批一批地进行训练。
train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)


# 定义自定义模型类，继承自 Keras 的 Model 类
class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        # 定义卷积层，输出通道为32，核大小为3x3，使用ReLU激活函数
        self.conv1 = Conv2D(32, 3, activation='relu')
        # 定义全连接层，输出节点为128
        self.flatten = Flatten()
        self.d1 = Dense(128, activation='relu')
        # 输出层，10个节点对应10个类别
        self.d2 = Dense(10)

    def call(self, x):
        # 前向传播，依次通过卷积层、全连接层和输出层
        x = self.conv1(x)
        x = self.flatten(x)
        x = self.d1(x)
        return self.d2(x)


# 实例化模型
model = MyModel()

# 定义损失函数为SparseCategoricalCrossentropy，用于多类别分类
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# 使用Adam优化器
optimizer = tf.keras.optimizers.Adam()

# 定义准确率指标
train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')


# 定义训练步骤
@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model(images)  # 获取模型预测
        loss = loss_object(labels, predictions)  # 计算损失
    gradients = tape.gradient(loss, model.trainable_variables)  # 计算梯度
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))  # 应用梯度
    train_loss(loss)  # 更新损失
    train_accuracy(labels, predictions)  # 更新准确率


# 定义测试步骤
@tf.function
def test_step(images, labels):
    predictions = model(images)  # 获取模型预测
    t_loss = loss_object(labels, predictions)  # 计算损失
    test_loss(t_loss)  # 更新损失
    test_accuracy(labels, predictions)  # 更新准确率


# 训练模型的主循环
EPOCHS = 5
for epoch in range(EPOCHS):
    # 在每个epoch开始时，重置指标
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    # 执行训练步骤
    for images, labels in train_ds:
        train_step(images, labels)

    # 执行测试步骤
    for test_images, test_labels in test_ds:
        test_step(test_images, test_labels)

    # 打印当前epoch的结果
    print(
        f'Epoch {epoch + 1}, '
        f'Loss: {train_loss.result()}, '
        f'Accuracy: {train_accuracy.result() * 100}, '
        f'Test Loss: {test_loss.result()}, '
        f'Test Accuracy: {test_accuracy.result() * 100}'
    )
