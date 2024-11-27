import cv2
import numpy as np
import os

def process_frame(frame, background, xmin, ymin, xmax, ymax, w, h):
    """
    將 frame 縮放到 w * h，並貼到 background 的 (xmin, ymin, xmax, ymax) 範圍內。
    """
    # 縮放 frame 到指定尺寸
    resized_frame = cv2.resize(frame, (w, h))
    
    # 建立一個背景的副本，避免修改原始背景
    output_frame = background.copy()
    
    # 確保貼圖區域大小與縮放尺寸一致
    overlay_height, overlay_width = ymax - ymin, xmax - xmin
    if (w, h) != (overlay_width, overlay_height):
        print("警告：貼圖區域與縮放尺寸不一致，調整貼圖區域尺寸。")
        w, h = overlay_width, overlay_height
        resized_frame = cv2.resize(frame, (w, h))

    # 將縮放的 frame 貼到指定範圍內
    output_frame[ymin:ymin + h, xmin:xmin + w] = resized_frame

    return output_frame

def process_video_with_overlay(input_path, background_path, output_path, xmin, ymin, xmax, ymax, w, h):
    # 讀取影片
    cap = cv2.VideoCapture(input_path)

    # 確認影片是否成功讀取
    if not cap.isOpened():
        print(f"無法打開影片：{input_path}")
        return

    # 讀取背景圖片
    background = cv2.imread(background_path)
    if background is None:
        print(f"無法打開背景圖片：{background_path}")
        return

    # 獲取影片屬性
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 確認背景大小是否正確
    frame_height, frame_width, _ = background.shape
    print(f"背景大小：寬度={frame_width}, 高度={frame_height}")
    
    # 定義影片編碼器和輸出影片
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 編碼格式
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # 逐幀處理影片
    frame_index = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # 處理影像
        processed_frame = process_frame(frame, background, xmin, ymin, xmax, ymax, w, h)

        # 寫入處理後的幀
        out.write(processed_frame)

        frame_index += 1
        print(f"處理中：{frame_index}/{frame_count}", end="\r")

    # 釋放資源
    cap.release()
    out.release()
    print("\n影片處理完成！")

# 使用範例
input_video = "testvideos/piano.mp4"  # 輸入影片路徑
background_image = "testimgs/1168.jpg"  # 背景圖片路徑
output_video = "output_overlay.mp4"  # 輸出影片路徑

# 指定貼圖區域和縮放尺寸
xmin, ymin, xmax, ymax = 695, 60, 869, 360  # 貼圖區域 (左上角和右下角座標)
w, h = xmax - xmin, ymax - ymin  # 縮放尺寸 (與貼圖區域一致)

# 執行影片處理
process_video_with_overlay(input_video, background_image, output_video, xmin, ymin, xmax, ymax, w, h)
