import pandas as pd
from collections import defaultdict
import re

file_path = './新建 文本文档.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

pattern = re.compile(r'<dt>(.*?)</dt>(.*?)<dl>', re.S)
area_matches = pattern.findall(content)

areas = defaultdict(list)

# Regular expression for small areas and their URLs within each big area
small_area_pattern = re.compile(r'<a href="(.*?)".*?title="(.*?)">')

for area in area_matches:
    big_area, area_content = area
    small_area_matches = small_area_pattern.findall(area_content)
    for url, small_area in small_area_matches:
        full_url = f"https://you.ctrip.com{url}"
        areas[big_area].append((small_area, full_url))

data = []
for big_area, small_areas in areas.items():
    for small_area, url in small_areas:
        data.append([big_area, small_area, url])

df = pd.DataFrame(data, columns=['Big Area', 'Small Area', 'URL'])

output_path = './areas_with_urls.xlsx'
df.to_excel(output_path, index=False)
