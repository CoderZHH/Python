import requests
from lxml import etree

# 目标URL
url = "https://you.ctrip.com/travels/Bali438/3998048.html"

# 设置headers模拟浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    print("Request successful!")

    # 解析HTML内容
    tree = etree.HTML(response.text)

    # 使用XPath找到class为'ctd_content'的div，递归提取其中所有的文本内容
    ctd_content_divs = tree.xpath("//div[@class='ctd_content']//text()")

    # 合并所有文本内容为一个字符串，并去除多余的空格和换行符
    # 先用split()将内容按空白字符切分，再用单一空格重新拼接
    content_text = ' '.join(''.join(ctd_content_divs).split())

    # 打印提取的纯文本内容
    print(content_text)

    # 将提取的文本内容保存到一个文本文件中
    with open('ctd_content.txt', 'w', encoding='utf-8') as f:
        f.write(content_text)

    print("Content successfully saved to 'ctd_content.txt'.")

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
