import requests
from bs4 import BeautifulSoup
import os
import time

# 設定目標 URL 模板
url_template = "https://ed.arte.gov.tw/ch/content/m_result_vlist_1.aspx?PageNo={}&AE_EPTY=視覺藝術&AE_MEDI={}"
category = "繪畫"

# 設定圖片存放資料夾
image_folder = f"dataset/台灣藝術教育網/{category}"
os.makedirs(image_folder, exist_ok=True)

# 定義標頭，模擬瀏覽器請求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 總頁數
total_pages = 48  # 根據您的描述

# 迴圈遍歷每一頁
for page in range(1, total_pages + 1):
    print(f"正在處理第 {page} 頁...")
    url = url_template.format(page, category)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    # 提取圖片連結
    image_tags = soup.find_all("img", class_="scale-with-grid wp-post-image")
    for img_tag in image_tags:
        img_src = img_tag.get("src")
        img_alt = img_tag.get("alt", "no_title")
        
        # 檢查 URL 格式，確保 img_src 開頭包含 '/'
        if img_src:
            # 若 img_src 已經包含完整的 URL 則直接使用，否則加上網站的根 URL
            if img_src.startswith("http"):
                img_url = img_src.replace("http://", "https://")
            else:
                img_url = f"https://ed.arte.gov.tw{img_src}"

            img_name = f"{img_alt}.jpg"
            img_path = os.path.join(image_folder, img_name)

            try:
                img_data = requests.get(img_url, headers=headers).content
                with open(img_path, "wb") as img_file:
                    img_file.write(img_data)
                print(f"已下載圖片：{img_name}")
            except Exception as e:
                print(f"下載圖片 {img_name} 時發生錯誤：{e}")
            

    # 為了避免對伺服器造成過大負擔，下載每頁後休息 1 秒
    time.sleep(2)

print("所有圖片下載完成。")
