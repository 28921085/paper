import requests
from bs4 import BeautifulSoup

# 目標網址
url = 'https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=B0000001'

# 發送 HTTP GET 請求
response = requests.get(url)
response.encoding = 'utf-8'  # 設定編碼以正確解析中文

# 檢查請求是否成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析網頁內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有條文的區域
    law_content = soup.find('div', {'class': 'law-reg-content'})

    if law_content:
        # 提取所有條文
        articles = law_content.find_all('div', {'class': 'row'})

        # 打開名為 law.txt 的檔案，使用 'w' 模式以寫入內容
        with open('law.txt', 'w', encoding='utf-8') as file:
            for article in articles:
                # 提取條號
                article_number = article.find('div', {'class': 'col-no'})
                # 提取條文內容
                article_content = article.find('div', {'class': 'col-data'})

                if article_number and article_content:
                    # 寫入條號和條文內容到檔案中，每條後加上兩個換行符號作為分隔
                    file.write(f"{article_number.get_text(strip=True)}\n")
                    file.write(f"{article_content.get_text(strip=True)}\n\n")
        print('法條內容已成功寫入 law.txt 檔案。')
    else:
        print('無法找到法條內容區域。')
else:
    print(f'無法訪問該網頁，狀態碼：{response.status_code}')
