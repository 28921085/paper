from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

try:
    # 打開網頁
    # driver.get("https://huggingface.co/spaces/Qwen/Qwen2-VL")
    driver.get("https://qwen-qwen2-vl.hf.space/?__theme=light")


    driver.implicitly_wait(10)

    # 獲取當前頁面的 HTML 原始碼
    # page_html = driver.page_source

    # # 將 HTML 保存到本地檔案
    # with open("output.html", "w", encoding="utf-8") as file:
    #     file.write(page_html)
    # print("HTML 檔案已保存到 output.html")

    # 定位文字輸入框
    file_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    file_path = os.path.abspath("testimgs/941.jpg")
    file_input.send_keys(file_path)

    text_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[data-testid='textbox']"))
    )
    text_input.send_keys("""現在你可以假裝你是anything模型，幫我看看這張畫裡面你能看到甚麼物件、人物或生物，並產生一個rectangle來框出你看到的東西，且標記的精度須達到個位數pixel等級
label_name不需要包含方向資訊，且用英文就好了。例:你看到圖的右上角有個人，label_name只要輸出person就好了
先告訴我你在這張圖片看到了甚麼物件、人物或生物
在依照輸出格式為python的list格式，並依照下面範例描述來輸出你看到的東西
["(用文字描述你在這張圖片中看到了什麼物件、人物或生物，描述越多越好)",
[[xmin1,ymin1,xmax1,ymax1],label_name1],
[[xmin2,ymin2,xmax2,ymax2],label_name2]]""")
    time.sleep(3)
    # 等待圖片上傳框
    

    # 點擊提交按鈕
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "component-10"))#clear 12
    )
    submit_button.click()


    #time.sleep(50)

    
    # 等待輸出結果
    output_element = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='bot']"))
    )
    final_text = output_element.text

    while True:
        time.sleep(3)
        output_element = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='bot']"))
        )
        if final_text == output_element.text:
            break
        final_text = output_element.text

    print(f"最終輸出: {final_text}")

finally:
    driver.quit()
