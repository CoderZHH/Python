import requests
from lxml import etree
import json

# 目标URL
url = "https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml"

# 构建查询参数
params = {
    "TravelId": 3998048,
    "IsReplyRefresh": 0,
    "ReplyPageNo": 1,
    "ReplyPageSize": 100,
    "_": 0000000000000
}

# 设置headers模拟浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 发送GET请求，并传递params
response = requests.get(url, headers=headers, params=params)

# 检查响应状态码
if response.status_code == 200:
    print("Request successful!")

    # 将响应的内容解析为JSON格式
    response_json = response.json()

    # 提取Html部分
    html_content = response_json.get("Html", "")

    # 解析提取的HTML内容
    tree = etree.HTML(html_content)

    # 提取评论的文本内容
    comments = tree.xpath("//p[@class='ctd_comments_text']/text()")

    # 存储所有的评论到数组
    cleaned_comments = []

    # 去除多余的换行符和空格，并将结果存入数组
    for comment in comments:
        # 去掉 \r\n，替换为单个空格，并去除前后多余的空格
        cleaned_comment = comment.replace("\r\n", " ").strip()
        cleaned_comments.append(cleaned_comment)

    # 输出数组
    print(cleaned_comments)

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
