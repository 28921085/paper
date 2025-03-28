import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 定義目標 URL
url = "https://web.arte.gov.tw/109sac/c1/ch1.html"
# 設定存儲資料夾的基礎路徑
dataset_path = "dataset/全國學生美術比賽"
os.makedirs(dataset_path, exist_ok=True)

# 記錄已下載圖片的 URL 和對應的獎項名稱
downloaded_images = {}

# 發送 GET 請求並解析內容
response = requests.get(url)
response.encoding = 'utf-8'  # 明確指定編碼為 UTF-8
soup = BeautifulSoup(response.text, "html.parser")

# 查找所有獎項連結
award_links = soup.select("ul li a[title]")

# 遍歷每個獎項
for award_link in award_links:
    award_name = award_link.get_text(strip=True)  # 獲取獎項名稱，例如 "特優"
    
    # 構建獎項頁面的完整 URL
    award_url = urljoin(url, award_link["href"])
    award_response = requests.get(award_url)
    award_response.encoding = 'utf-8'  # 明確指定編碼為 UTF-8
    award_soup = BeautifulSoup(award_response.text, "html.parser")
    
    # 查找該獎項頁面上的所有圖片連結
    img_links = award_soup.find_all("a", href=True)

    for img_link in img_links:
        # 嘗試從 <a> 標籤的 href 獲取原圖 URL
        img_page_url = urljoin(award_url, img_link["href"])
        img_page_response = requests.get(img_page_url)
        img_page_response.encoding = 'utf-8'
        img_page_soup = BeautifulSoup(img_page_response.text, "html.parser")
        
        # 在圖片頁面中查找原圖的 URL
        img_tag = img_page_soup.find("img")
        if img_tag:
            img_url = img_tag.get("src")
            full_img_url = urljoin(img_page_url, img_url)

            # 如果圖片已經被記錄過，則跳過
            if full_img_url in downloaded_images:
                continue

            # 取得圖片名稱，並移除不允許的字符
            img_name = os.path.basename(img_url)
            img_name = re.sub(r'[<>:"/\\|?*]', "", img_name)  # 移除 Windows 不允許的字符
            
            # 過濾掉副檔名不是 .jpg 的圖片
            if not img_name.lower().endswith(".jpg"):
                continue
            
            # 記錄 URL 和對應的獎項名稱
            downloaded_images[full_img_url] = f"{award_name}_{img_name}"

# 遍歷字典並下載圖片
for img_url, img_save_name in downloaded_images.items():
    # 設定圖片儲存的完整路徑
    img_save_path = os.path.join(dataset_path, img_save_name)
    
    # 發送請求以抓取圖片
    img_data = requests.get(img_url).content
    
    # 將圖片儲存到本地資料夾
    with open(img_save_path, "wb") as img_file:
        img_file.write(img_data)
    print(f"已儲存圖片: {img_save_path}")

print("圖片抓取完成！")
