import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

url = "http://ed.arte.gov.tw/ae/ae2023/繪畫甲等-A5郭姝岑.jpg"
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))

try:
    response = session.get(url, timeout=10)
    if response.status_code == 200:
        with open("image.jpg", "wb") as file:
            file.write(response.content)
        print("圖片下載完成")
    else:
        print("圖片下載失敗，狀態碼:", response.status_code)
except requests.exceptions.RequestException as e:
    print(f"請求發生錯誤: {e}")
