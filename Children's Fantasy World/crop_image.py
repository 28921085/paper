import cv2
import os
import numpy as np
import sys
import re
sys.path.append("../Common Module")
from load_data import LoadData
from write_data import WriteData

# 原始圖片的路徑
image_path = os.path.abspath('testimgs/優等_1050.jpg')

# 載入原始圖片
image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)

# 確認圖片是否成功載入
if image is None:
    raise FileNotFoundError(f"無法載入圖片：{image_path}")

# 獲取圖片的實際尺寸
image_height, image_width = image.shape[:2]

# 定義座標的最大範圍
max_range = 1000

# 從檔案讀取座標和標籤資料（忽略第一行）
file_path = 'run/bbox27/response.txt'
coordinates = []
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()[1:]  # 跳過第一行
    for line in lines:
        line = line.strip()
        if line:
            # 用正則表達式將非數字的部分替換為空格
            cleaned_line = re.sub(r"[^\d]", " ", line)
            # 依據空格切分，過濾出非空字串並取前 4 個數字
            coords = [int(num) for num in cleaned_line.split()[:4]]
            # 縮放座標到圖片比例
            scaled_coords = [
                int(coords[0] * image_width / max_range),  # xmin
                int(coords[1] * image_height / max_range),  # ymin
                int(coords[2] * image_width / max_range),  # xmax
                int(coords[3] * image_height / max_range)  # ymax
            ]
            # 處理標籤（提取原始標籤）
            label = line.rsplit(",", 1)[-1].strip().strip("'[]")  # 保留標籤
            # 儲存座標與標籤
            coordinates.append([scaled_coords, label])

# 創建保存裁剪圖片的資料夾
output_dir = 'cropped_images'
os.makedirs(output_dir, exist_ok=True)
writer = WriteData(prefix="crop")

# 迭代座標資料，進行裁剪並保存
for idx, (coord, label) in enumerate(coordinates):
    xmin, ymin, xmax, ymax = coord
    # 確保裁剪區域不超出圖片邊界
    xmin, ymin, xmax, ymax = max(0, xmin), max(0, ymin), min(image_width, xmax), min(image_height, ymax)
    # 裁剪圖片
    cropped_image = image[ymin:ymax, xmin:xmax]
    writer.save_img_cv2(cropped_image, f'{idx}.jpg')
    print(f"已保存裁剪圖片：{idx}.jpg")
