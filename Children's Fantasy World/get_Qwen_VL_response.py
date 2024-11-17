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
    text_input.send_keys("在這張圖上你看到了什麼")
    time.sleep(3)
    # 等待圖片上傳框
    

    # 點擊提交按鈕
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "component-10"))#clear 12
    )
    submit_button.click()


    time.sleep(50)
    # 等待輸出結果
    output_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='bot']"))
    )
   

    print(f"最終輸出: {output_element.text}")

finally:
    driver.quit()
