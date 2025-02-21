import yt_dlp
import os

def download_youtube_video(url, save_path="downloads"):
    os.makedirs(save_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'mp4',  # 確保下載 MP4 格式
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'  # 確保影片轉換為標準 MP4
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("請輸入 YouTube 影片網址: ")
    download_youtube_video(video_url)
