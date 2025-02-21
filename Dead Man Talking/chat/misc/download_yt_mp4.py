import yt_dlp
import os

def download_youtube_video(url, save_path="downloads"):
    os.makedirs(save_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("請輸入 YouTube 影片網址: ")
    download_youtube_video(video_url)
