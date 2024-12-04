import pickle

def load_cookies(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)

def compare_cookies(cookies1, cookies2):
    cookies1_dict = {cookie['name']: cookie for cookie in cookies1}
    cookies2_dict = {cookie['name']: cookie for cookie in cookies2}

    all_keys = set(cookies1_dict.keys()).union(set(cookies2_dict.keys()))

    differences = []
    for key in all_keys:
        cookie1 = cookies1_dict.get(key)
        cookie2 = cookies2_dict.get(key)
        if cookie1 != cookie2:
            differences.append((cookie1, cookie2))

    return differences

# 读取两个 cookies.pkl 文件
cookies1 = load_cookies("cookies1.pkl")
cookies2 = load_cookies("cookies2.pkl")

# 比较 cookies 并输出不同之处
differences = compare_cookies(cookies1, cookies2)
for cookie1, cookie2 in differences:
    print(f"Cookie 名称: {cookie1['name'] if cookie1 else cookie2['name']}")
    print(f"Cookies1: {cookie1}")
    print(f"Cookies2: {cookie2}")
    print("-" * 40)