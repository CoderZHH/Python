import pickle
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import random
import json
import requests
import os


# 定义一个随机等待的函数
def random_wait(min_seconds=2, max_seconds=5):
    """
    在 min_seconds 和 max_seconds 之间随机等待。
    :param min_seconds: 最小等待时间（秒）
    :param max_seconds: 最大等待时间（秒）
    """
    wait_time = random.uniform(min_seconds, max_seconds)  # 生成 min_seconds 和 max_seconds 之间的随机浮点数
    print(f"等待 {wait_time:.2f} 秒...")
    time.sleep(wait_time)  # 等待指定的时间


# 启动浏览器并访问目标网址
def start_browser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # 浏览器保持打开
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.xuexi.cn/')
    return driver


# 保存 Cookies 到文件
def save_cookies(driver, filename):
    try:
        cookies = driver.get_cookies()  # 获取当前会话中的所有 cookies
        with open(filename, 'wb') as file:
            pickle.dump(cookies, file)
        print(f"Cookies 已保存到 {filename}")
    except Exception as e:
        print(f"保存 cookies 时出错：{e}")


# 加载 Cookies 并添加到浏览器会话中
def load_cookies(driver, filename):
    try:
        with open(filename, 'rb') as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']  # 删除 expiry 字段
            driver.add_cookie(cookie)  # 添加每个 cookie
        print("Cookies 已加载成功")
    except Exception as e:
        print(f"加载 cookies 时出错：{e}")


# 扫码登录并保存 cookies
def manual_login(driver, filename):
    try:
        # 查找并点击登录按钮
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-icon"))
        )
        login_button.click()
        print("登录按钮已点击，正在等待扫码登录...")

        switch_to_new_window(driver)

        # 等待用户扫码并成功登录
        WebDriverWait(driver, 60).until(EC.url_contains("https://www.xuexi.cn/"))
        print("扫码登录成功")

        # 保存 cookies
        save_cookies(driver, filename)

        # 关闭登录界面
        close_additional_windows(driver)

    except Exception as e:
        print(f"扫码登录时出错：{e}")


# 切换到新打开的窗口或标签页
def switch_to_new_window(driver):
    random_wait(1, 5)  # 随机等待 1~5 秒
    # 获取当前所有窗口句柄
    current_window = driver.current_window_handle
    all_windows = driver.window_handles

    # 切换到新窗口
    for window in all_windows:
        if window != current_window:
            driver.switch_to.window(window)
            print("已切换到新窗口")
            break


def close_additional_windows(driver):
    random_wait(1, 5)  # 随机等待 1~5 秒
    # 获取当前所有窗口句柄
    all_windows = driver.window_handles

    # 第一个窗口是主窗口
    main_window = all_windows[0]

    # 遍历所有窗口句柄，关闭从第二个开始的窗口
    for window in all_windows[1:]:
        driver.switch_to.window(window)
        driver.close()
        print(f"关闭所有窗口")

    # 切换回主窗口
    driver.switch_to.window(main_window)
    print("已切换回主窗口")


# 模拟鼠标点击 "我的积分"
def click_points(driver):
    random_wait(1, 5)  # 随机等待 1~5 秒
    try:
        # 等待页面加载并找到目标元素
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '我的积分')]"))
        )
        # 创建 ActionChains 对象
        actions = ActionChains(driver)
        # 模拟鼠标移动并点击该元素
        actions.move_to_element(element).click().perform()
        print("成功点击 '我的积分'")

        # 切换到新窗口或标签页
        switch_to_new_window(driver)
        poitnts = gei_points(driver)
        close_additional_windows(driver)
        return poitnts
    except Exception as e:
        print(f"点击 '我的积分' 时出错：{e}")


def gei_points(driver):
    try:
        random_wait(5, 10)  # 随机等待 5~10 秒
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='my-points-card-text']"))
        )
        points_texts = [element.text for element in elements]
        return points_texts
    except Exception as e:
        print(f"获取‘我的积分’文本时出错：{e}")


# 刷分
def progress(driver):
    while True:
        # 点击 "我的积分" 并获取积分
        points = click_points(driver)
        print(f"当前积分: {points}")

        # 解析当前分数和目标分数
        scores = [int(point.split('/')[0].replace('分', '')) for point in points]
        targets = [int(point.split('/')[1].replace('分', '')) for point in points]

        # 标记是否所有任务已完成
        all_tasks_done = True

        # 任务2：阅读文章
        if scores[1] < targets[1]:
            print(f"任务2：当前得分 {scores[1]}，目标得分 {targets[1]}，开始执行任务2...")
            task2(driver, score_target=targets[1] - scores[1])
            all_tasks_done = False  # 任务未完成，需要继续循环

        # 任务3：观看视频
        if scores[2] < targets[2]:
            print(f"任务3：当前得分 {scores[2]}，目标得分 {targets[2]}，开始执行任务3...")
            task3(driver, score_target=targets[2] - scores[2])
            all_tasks_done = False  # 任务未完成，需要继续循环

        # 任务4：每日答题
        if scores[3] < targets[3]:
            print(f"任务4：当前得分 {scores[3]}，目标得分 {targets[3]}，开始执行任务4...")
            task4(driver)
            all_tasks_done = False  # 任务未完成，需要继续循环

        # 如果所有任务都已完成，则跳出循环
        if all_tasks_done:
            print("所有任务已完成！")
            driver.quit()  # 关闭浏览器
            break

        # 随机等待一段时间再重新获取积分
        random_wait(5,10)


# 任务2：阅读文章
def task2(driver, score_target=12):
    random_wait(1, 5)  # 随机等待 1~5 秒
    score = 0
    json_data = driver.execute_script("""
        return fetch('https://www.xuexi.cn/lgdata/1ap1igfgdn2.json')
               .then(response => response.json())
               .then(data => data);
    """)

    # 提取文章的 URL 列表
    url_list = [item['url'] for item in json_data]

    # 随机选择前 50 条 URL
    url_list = random.sample(url_list, min(50, len(url_list)))

    print("开始阅读文章...")
    for url in url_list:
        if score >= score_target:
            print(f"已达到目标分数: {score}")
            break

        # 打开文章 URL
        print(f"访问文章: {url}")
        main_window = driver.current_window_handle  # 获取当前窗口句柄
        driver.execute_script(f"window.open('{url}', '_blank');")  # 在新标签页中打开文章
        switch_to_new_window(driver)  # 切换到新打开的窗口
        ##################################################################################### 模拟鼠标和滚轮操作，阅读文章

        # 在页面停留 70 到 80 秒
        random_wait(70, 80)

        # 关闭文章窗口并切换回主窗口
        driver.close()
        driver.switch_to.window(main_window)  # 切换回主窗口

        # 积分增加
        score += 2
        print(f"当前得分: {score}")

    return score

# 任务3：观看视频
def task3(driver, score_target=12):
    random_wait(1, 5)  # 随机等待 1~5 秒
    score = 0
    json_data_url = 'https://www.xuexi.cn/lgdata/1742g60067k.json'  # 视频 JSON 数据的 URL

    # 从页面中获取 JSON 数据
    json_data = driver.execute_script(f"""
        return (async function() {{
            const response = await fetch('{json_data_url}');
            const data = await response.json();
            return data;
        }})();
    """)

    if not json_data:
        print("未能获取视频列表")
        return

    # 提取视频的 URL 列表
    url_list = [item['url'] for item in json_data]

    # 随机选择前 50 条 URL
    url_list = random.sample(url_list, min(50, len(url_list)))

    print("开始观看视频...")
    for url in url_list:
        if score >= score_target:
            print(f"已达到目标分数: {score}")
            break

        # 打开视频 URL
        print(f"访问视频: {url}")
        main_window = driver.current_window_handle  # 获取当前窗口句柄
        driver.execute_script(f"window.open('{url}', '_blank');")  # 在新标签页中打开视频
        switch_to_new_window(driver)  # 切换到新打开的窗口

        # 在页面上找到播放按钮并点击播放
        try:
            # 查找播放按钮元素，确保页面加载完成
            play_button = WebDriverWait(driver, 40).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "prism-big-play-btn"))
            )

            # 模拟点击播放按钮
            actions = ActionChains(driver)
            actions.move_to_element(play_button).click().perform()
            print("视频开始播放...")

            # 停留在页面 70 到 80 秒
            random_wait(70, 80)

        except Exception as e:
            print(f"无法找到播放按钮或播放视频时出错: {e}")

        # 关闭视频页面并切换回主窗口
        driver.close()
        driver.switch_to.window(main_window)  # 切换回主窗口

        # 积分增加
        score += 2
        print(f"当前得分: {score}")

    return score

# 任务4：每日答题
def task4(driver):
    random_wait(1, 5)  # 随机等待 1~5 秒
    print("开始每日答题...")
    exam_url = 'https://pc.xuexi.cn/points/exam-practice.html'

    main_window = driver.current_window_handle  # 获取当前窗口句柄

    # 打开考试页面
    driver.execute_script(f"window.open('{exam_url}', '_blank');")
    switch_to_new_window(driver)

    # 等待页面加载完成
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "ant-btn")))
    print("考试页面加载完成，准备执行脚本...")

    # 读取并执行外部 JS 脚本
    script_file = "./xuexi_script.js"  # JavaScript 文件路径
    if os.path.exists(script_file):
        try:
            with open(script_file, 'r', encoding='utf-8') as js_file:
                script_content = js_file.read()  # 读取文件内容
                driver.execute_script(script_content)  # 执行 JavaScript 脚本
            print(f"已成功执行 {script_file} 中的脚本")
        except Exception as e:
            print(f"执行脚本时出错: {e}")
    else:
        print(f"脚本文件 {script_file} 不存在！")

    # 停留足够时间让脚本运行
    random_wait(40, 40)  # 根据脚本需要调整等待时间，300秒=5分钟

    # 关闭考试页面并切换回主窗口
    driver.close()
    driver.switch_to.window(main_window)  # 切换回主窗口
    print("已关闭考试页面，返回主窗口")

# 主流程：可以选择扫码登录或使用保存的 Cookies 登录
def main():
    driver = start_browser()  # 启动浏览器
    filename = "cookies1.pkl"  # 定义 cookies 文件名

    if not os.path.exists(filename):
        print("cookies 文件不存在，开始扫码登录")
        manual_login(driver, filename)  # 执行扫码登录并保存
    else:
        load_cookies(driver, filename)
        driver.refresh()  # 刷新页面以使用 cookies
        print("使用 Cookies 登录中...")


    # 开始刷分
    progress(driver)

    # 关闭浏览器
    # driver.quit()


if __name__ == "__main__":
    main()  # 运行主流程

# 新闻视频列表
# const VideosUrl2 = "https://www.xuexi.cn/lgdata/1742g60067k.json";

# 每日答题页面
# const ExamPracticeUrl = "https://pc.xuexi.cn/points/exam-practice.html";

# 学习时评新闻列表
# const NewsUrl2 = "https://www.xuexi.cn/lgdata/1ap1igfgdn2.json";
