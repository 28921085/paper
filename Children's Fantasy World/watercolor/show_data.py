import os
import cv2
import xml.etree.ElementTree as ET
import random

print("當前工作路徑:", os.getcwd())

# 設定資料集路徑
dataset_path = r"E:\paper\Children's Fantasy World\dataset\Watercolor2k"

# 圖像和標註路徑
images_path = os.path.join(dataset_path, 'JPEGImages')
annotations_path = os.path.join(dataset_path, 'Annotations')

# 獲取所有圖像文件名
image_files = [f for f in os.listdir(images_path) if f.endswith('.jpg')]

# 隨機選擇10張圖像
random_images = random.sample(image_files, 10)

for image_file in random_images:
    # 讀取圖像
    image_path = os.path.join(images_path, image_file)
    image = cv2.imread(image_path)

    # 對應的標註文件
    annotation_file = image_file.replace('.jpg', '.xml')
    annotation_path = os.path.join(annotations_path, annotation_file)

    # 解析標註文件
    tree = ET.parse(annotation_path)
    root = tree.getroot()

    print(f"\n圖像文件: {image_file}")
    
    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # 印出標註的類別和位置
        print(f"標註: 類別 = {name}, 位置 = (xmin: {xmin}, ymin: {ymin}, xmax: {xmax}, ymax: {ymax})")

        # 在圖像上繪製邊界框
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(image, name, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # 顯示圖像
    cv2.imshow('Image', image)
    cv2.waitKey(0)

cv2.destroyAllWindows()
