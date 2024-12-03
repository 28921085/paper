import cv2
import numpy as np
import os

def create_mask_for_inpainting(background, xmin, ymin, xmax, ymax, margin=20, probability=0.7):
    """
    創建一個 mask，其中 (xmin, ymin, xmax, ymax) 所圍成的 1px 框框是 100% 成為白色 mask，
    其餘範圍內外 margin 部分依然按指定機率成為白色。
    
    :param background: 背景圖片（用來確定大小）
    :param xmin: 左上角 x 座標
    :param ymin: 左上角 y 座標
    :param xmax: 右下角 x 座標
    :param ymax: 右下角 y 座標
    :param margin: 周圍範圍的像素大小（內外同時應用）
    :param probability: 每個像素成為 mask 的機率 (0~1 之間)
    :return: 生成的 mask
    """
    # 初始化與背景相同大小的黑色 mask
    mask = np.zeros(background.shape[:2], dtype=np.uint8)

    # 外部範圍
    outer_start_x = max(0, xmin - margin)
    outer_start_y = max(0, ymin - margin)
    outer_end_x = min(background.shape[1], xmax + margin)
    outer_end_y = min(background.shape[0], ymax + margin)

    # 內部範圍
    inner_start_x = min(background.shape[1], max(0, xmin + margin))
    inner_start_y = min(background.shape[0], max(0, ymin + margin))
    inner_end_x = max(0, min(background.shape[1], xmax - margin))
    inner_end_y = max(0, min(background.shape[0], ymax - margin))

    # 填充外部範圍 (外部區域)
    outer_region_height = outer_end_y - outer_start_y
    outer_region_width = outer_end_x - outer_start_x
    random_outer_mask = np.random.choice([0, 255], size=(outer_region_height, outer_region_width), p=[1 - probability, probability]).astype(np.uint8)
    mask[outer_start_y:outer_end_y, outer_start_x:outer_end_x] = random_outer_mask

    # 清空內部範圍 (內部不包含)
    mask[inner_start_y:inner_end_y, inner_start_x:inner_end_x] = 0

    # 設置框框的 1px 範圍為 100% 白色
    mask[ymin:ymin + 1, xmin:xmax + 1] = 255  # 上邊
    mask[ymax:ymax + 1, xmin:xmax + 1] = 255  # 下邊
    mask[ymin:ymax + 1, xmin:xmin + 1] = 255  # 左邊
    mask[ymin:ymax + 1, xmax:xmax + 1] = 255  # 右邊

    return mask




def process_frame_with_inpaint(frame, background, xmin, ymin, xmax, ymax, w, h):
    """
    將 frame 縮放到 w * h，貼到背景上，並對指定範圍進行 inpaint 修補。
    """
    # 縮放 frame 到指定尺寸
    resized_frame = cv2.resize(frame, (w, h))

    # 建立背景副本
    output_frame = background.copy()

    # 確保貼圖區域大小與縮放尺寸一致
    overlay_height, overlay_width = ymax - ymin, xmax - xmin
    if (w, h) != (overlay_width, overlay_height):
        print("警告：貼圖區域與縮放尺寸不一致，調整貼圖區域尺寸。")
        w, h = overlay_width, overlay_height
        resized_frame = cv2.resize(frame, (w, h))

    # 將縮放的 frame 貼到指定範圍內
    output_frame[ymin:ymin + h, xmin:xmin + w] = resized_frame

    # 創建 mask
    mask = create_mask_for_inpainting(background, xmin, ymin, xmax, ymax)

    # 使用 inpaint 修補區域周圍
    inpainted_frame = cv2.inpaint(output_frame, mask, inpaintRadius=3, flags=cv2.INPAINT_NS)
    # inpainted_frame = cv2.inpaint(output_frame, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)


    return inpainted_frame

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
        processed_frame = process_frame_with_inpaint(frame, background, xmin, ymin, xmax, ymax, w, h)

        # 寫入處理後的幀
        out.write(processed_frame)

        frame_index += 1
        print(f"處理中：{frame_index}/{frame_count}", end="\r")

    # 釋放資源
    cap.release()
    out.release()
    print("\n影片處理完成！")

# 使用範例
# input_video = "testvideos/piano.mp4"  # 輸入影片路徑
input_video = "https://dnznrvs05pmza.cloudfront.net/42e6b708-c285-4207-9ada-72da11e32033.mp4?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiZWY3OTgxY2RkYjc0MGVlNyIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTczMzM1NjgwMH0._sQI5Yk_cBvSNVZI4cfde3SVvCLFyjhq9lVO50u65fY"  # 輸入影片路徑
# input_video = "https://dnznrvs05pmza.cloudfront.net/af612978-7043-4638-b952-fe8699725353.mp4?_jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlIYXNoIjoiNzg4ZjY3YTkyNmM5YjQyZCIsImJ1Y2tldCI6InJ1bndheS10YXNrLWFydGlmYWN0cyIsInN0YWdlIjoicHJvZCIsImV4cCI6MTczMzM1NjgwMH0.2SN9q5iZR-fgF6zKgsykce1X3eGuPLiQNTjB6IGH-_E"
background_image = "testimgs/1168.jpg"  # 背景圖片路徑
output_video = "output_overlay.mp4"  # 輸出影片路徑

# 指定貼圖區域和縮放尺寸
xmin, ymin, xmax, ymax = 695, 60, 869, 360  # 貼圖區域 (左上角和右下角座標)
w, h = xmax - xmin, ymax - ymin  # 縮放尺寸 (與貼圖區域一致)

# 執行影片處理
process_video_with_overlay(input_video, background_image, output_video, xmin, ymin, xmax, ymax, w, h)
