import pandas as pd
media6 = pd.read_csv('../tmp/media4.csv', header='infer')

# 基于流行度的推荐算法
from sklearn.model_selection import train_test_split
# 将数据划分为训练集测试集
media6_train, media6_test = train_test_split(media6, test_size=0.2, random_state=1234)

# 将节目按热度排名
program = media6_train.program_title.value_counts()
program = program.reset_index()
program.columns = ['program', 'counts']

recommend_dataframe = pd.DataFrame
m = 3000
# 对输入的用户名进行判断，若输入为0，则停止运行，否则展示输入的用户名所对应推荐的节目
while True:
    input_no = int(input('Please input one phone_no that is not in group:'))
    if input_no == 0:
        print('Stop recommend!')
        break
    else:
        recommend_dataframe = pd.DataFrame(program.iloc[:m, 0], columns=['program'])
        print('Phone_no is %d. \nRecommend_list is \n' % (input_no), 
              recommend_dataframe)
'''
当输入16801274792时，即可为用户名为16801274792的用户，推荐推荐最热门的前N个节目
当输入0时，即可结束为用户进行推荐
'''





