import requests
from lxml import etree
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor

# 设置headers模拟浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def fetch_page_data(url, params, headers):
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"获取页面 {params['p']} 失败。状态码:", response.status_code)
        return None


def parse_html(html):
    tree = etree.HTML(html)
    city_divs = tree.xpath("//div[@class='city']")
    page_results = []

    for div in city_divs:
        title = div.xpath(".//a[@class='cpt']/@title")
        title = title[0] if title else None

        traveldate = div.xpath(".//i[@class='time']/text()")
        traveldate = traveldate[0] if traveldate else None

        author = div.xpath(".//div[@class='authorinfo']//a[2]/@title")
        author = author[0] if author else None
        weburl = div.xpath(".//div[@class='authorinfo']//a[2]/@href")
        weburl = weburl[0] if weburl else None

        city = div.xpath(".//a[@class='city-name']/text()")
        city = city[0] if city else None

        result = {
            "title": title,
            "city": city,
            "traveldate": traveldate,
            "author": author,
            "weburl": weburl
        }
        page_results.append(result)

    return page_results


def extract_longtext(weburl):
    if not weburl:
        return None

    response = requests.get(weburl, headers=headers)
    if response.status_code == 200:
        tree = etree.HTML(response.text)
        ctd_content_divs = tree.xpath("//div[@class='ctd_content']//text()")
        content_text = ' '.join(''.join(ctd_content_divs).split())
        return content_text
    else:
        print(f"从 {weburl} 获取内容失败。状态码: {response.status_code}")
        return None


def extract_comments(travel_id):
    url = "https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml"
    params = {
        "TravelId": travel_id,
        "IsReplyRefresh": 0,
        "ReplyPageNo": 1,
        "ReplyPageSize": 100,
        "_": int(time.time() * 1000)
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response_json = response.json()
        html_content = response_json.get("Html", "")
        tree = etree.HTML(html_content)
        comments = tree.xpath("//p[@class='ctd_comments_text']/text()")

        cleaned_comments = [comment.replace("\r\n", " ").strip() for comment in comments]
        return cleaned_comments
    else:
        print(f"获取 TravelId 为 {travel_id} 的评论失败。状态码: {response.status_code}")
        return []


def extract_code_from_url(weburl):
    match = re.search(r'/([^/]+)\.html', weburl)
    if match:
        return match.group(1)
    return None


def process_page_result(result):
    weburl = result.get("weburl")
    if weburl:
        print(f"正在处理 {result['title']} 的长文本内容和评论，网址: {weburl}")
        result["longtext"] = extract_longtext(weburl)

        travel_id = extract_code_from_url(weburl)
        if travel_id:
            print(f"正在提取 TravelId 为 {travel_id} 的评论...")
            result["comments"] = extract_comments(travel_id)


def main():
    # 记录程序开始时间
    start_time = time.time()

    url = "https://you.ctrip.com/TravelSite/Home/IndexTravelListHtml"
    all_results = []

    # 创建线程池
    with ThreadPoolExecutor(max_workers=5) as executor:
        for page in range(1, 6):
            params = {
                "p": page,
                "Idea": 0,
                "Type": 100,
                "Plate": 0
            }

            html = fetch_page_data(url, params, headers)
            if html:
                page_results = parse_html(html)
                all_results.extend(page_results)

                # 并发处理每个页面的 longtext 和 comments 提取
                executor.map(process_page_result, page_results)

    # 保存结果到JSON文件
    save_to_json(all_results, 'results.json')

    # 记录程序结束时间
    end_time = time.time()

    # 计算并输出总耗时
    print(f"总耗时: {end_time - start_time:.2f} 秒")


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"JSON数据已成功保存到 '{filename}' 文件中。")


if __name__ == "__main__":
    main()
