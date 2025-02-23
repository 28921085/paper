import os
import shutil
import sys
from download_yt_mp4 import download_youtube_video
from mp4tomp3 import convert_mp4_to_mp3

def main():
    video_url = input("請輸入 YouTube 影片網址: ")
    custom_name = input("請輸入要儲存的影片檔名（可留空使用預設標題）: ").strip()

    # 下載影片，允許使用者指定檔名
    print("正在下載影片...")
    mp4_file_path = download_youtube_video(video_url, custom_name if custom_name else None)

    if not os.path.exists(mp4_file_path):
        print("下載失敗，找不到影片")
        sys.exit(1)

    print(f"下載完成: {mp4_file_path}")

    # 轉換 MP4 為 MP3
    mp3_file_path = convert_mp4_to_mp3(mp4_file_path)
    if mp3_file_path is None:
        print("轉換 MP3 失敗")
        sys.exit(1)

    # 準備移動檔案
    save_path = "downloads"
    os.makedirs(save_path, exist_ok=True)  # 確保 `downloads/` 資料夾存在

    # 移動 MP4 檔案
    new_mp4_path = os.path.join(save_path, os.path.basename(mp4_file_path))
    shutil.move(mp4_file_path, new_mp4_path)
    print(f"已移動 MP4: {new_mp4_path}")

    # 移動 MP3 檔案
    new_mp3_path = os.path.join(save_path, os.path.basename(mp3_file_path))
    shutil.move(mp3_file_path, new_mp3_path)
    print(f"已移動 MP3: {new_mp3_path}")

if __name__ == "__main__":
    main()
