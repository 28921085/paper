import cv2
from deepface import DeepFace
from tqdm import tqdm

# 打开视频文件
video_path = 'video_short.mp4'
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("无法打开视频文件")
    exit()

# 获取视频的总帧数
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# 打开文本文件用于写入，指定编码为 UTF-8
with open('video.txt', 'w', encoding='utf-8') as file:
    # 使用 tqdm 包装帧读取循环，显示进度条
    for _ in tqdm(range(total_frames), desc="Processing Video"):
        ret, frame = cap.read()
        if not ret:
            break

        # 获取当前帧的时间戳（以毫秒为单位）
        timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        # 将时间戳转换为秒
        timestamp_sec = timestamp_ms / 1000.0

        try:
            # 使用 DeepFace 对当前帧进行情绪分析
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

            # 检查 analysis 的类型
            if isinstance(analysis, list):
                # 如果是列表，取第一个元素
                analysis = analysis[0]

            # 获取主要情绪
            dominant_emotion = analysis['dominant_emotion']

            # 将时间戳和情绪结果写入文件
            file.write(f'Time: {timestamp_sec:.2f} sec, Emotion: {dominant_emotion}\n')
        except Exception as e:
            print(f'分析失败: {e}')
            # 将错误信息写入文件
            file.write(f'Time: {timestamp_sec:.2f} sec, Emotion: 分析失败\n')

# 释放视频捕获对象
cap.release()
