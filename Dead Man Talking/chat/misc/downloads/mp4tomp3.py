import os
import ffmpeg

def convert_mp4_to_mp3(mp4_file_path, output_folder="downloads"):
    try:
        # 創建輸出資料夾
        os.makedirs(output_folder, exist_ok=True)
        
        # 設定 MP3 輸出路徑
        mp3_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(mp4_file_path))[0] + ".mp3")
        
        print("開始轉換為 MP3...")
        (
            ffmpeg.input(mp4_file_path)
            .output(mp3_file_path, format='mp3', audio_bitrate='192k')
            .run(overwrite_output=True, quiet=True)
        )
        
        print(f"轉換完成：{mp3_file_path}")
        return mp3_file_path
        
    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    mp4_path = input("請輸入 MP4 檔案路徑: ")
    convert_mp4_to_mp3(mp4_path)
