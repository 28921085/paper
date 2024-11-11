import requests

url = "http://ed.arte.gov.tw/ae/ae2023/繪畫甲等-A5郭姝岑.jpg"
response = requests.get(url)

if response.status_code == 200:
    with open("image.jpg", "wb") as file:
        file.write(response.content)
    print("圖片下載完成")
else:
    print("圖片下載失敗，狀態碼:", response.status_code)
