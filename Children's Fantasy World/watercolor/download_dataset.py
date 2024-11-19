import subprocess
import zipfile
import os

# 定義要下載的檔案 ID 和對應的名稱
file_ids = [
    ("1LvxwCOfUa-OklIvBJhB8zJlochjJiPFS", "clipart.zip"),
    ("1fa2L6oaPSjZ1_WqlTmIp6i2RbdR2y1Pw", "watercolor.zip"),
    ("1bZtVWcxxFrijE_ALvNPjH1MXIKio6BIr", "comic.zip")
]

# 下載檔案
for file_id, file_name in file_ids:
    print(f"正在下載 {file_name}...")
    subprocess.run(["gdown", file_id], check=True)

# 解壓縮並刪除壓縮檔
for _, file_name in file_ids:
    print(f"正在解壓縮 {file_name}...")
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()
    os.remove(file_name)
    print(f"{file_name} 已刪除。")

print("所有檔案已下載並解壓縮完成。")
