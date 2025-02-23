import yt_dlp
import os
import re

def sanitize_filename(filename):
    """移除檔名中的特殊字元"""
    return re.sub(r'[\/:*?"<>|【】]', '', filename)

def download_youtube_video(url, custom_filename=None):
    """下載 YouTube 影片，允許指定檔案名稱"""
    current_folder = os.getcwd()  # 獲取當前目錄

    # 如果有提供自訂名稱，則使用該名稱，否則使用 YouTube 標題
    if custom_filename:
        clean_title = sanitize_filename(custom_filename)
    else:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            clean_title = sanitize_filename(info_dict.get('title', 'unknown'))

    filename = f"{clean_title}.mp4"
    output_path = os.path.join(current_folder, filename)

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': output_path,  # 直接指定下載檔案名稱
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"影片已下載：{output_path}")
    return output_path  # 回傳 MP4 檔案的完整路徑

if __name__ == "__main__":
    video_url = input("請輸入 YouTube 影片網址: ")
    custom_name = input("請輸入要儲存的影片檔名（可留空使用預設標題）: ").strip()
    downloaded_file = download_youtube_video(video_url, custom_name if custom_name else None)
    print(f"下載完成: {downloaded_file}")
