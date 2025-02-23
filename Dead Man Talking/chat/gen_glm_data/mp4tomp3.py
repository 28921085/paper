import os
import ffmpeg

def convert_mp4_to_mp3(mp4_file_path):
    try:
        # 取得 MP4 檔案的資料夾
        input_folder = os.path.dirname(mp4_file_path)

        # 設定 MP3 輸出路徑（與 MP4 相同資料夾）
        mp3_file_path = os.path.join(input_folder, os.path.splitext(os.path.basename(mp4_file_path))[0] + ".mp3")
        
        print("開始轉換為 MP3...")
        (
            ffmpeg.input(mp4_file_path)
            .output(mp3_file_path, format='mp3', audio_bitrate='192k')
            .run(overwrite_output=True, quiet=True)
        )
        
        print(f"轉換完成：{mp3_file_path}")
        return mp3_file_path  # 回傳轉換後的 MP3 檔案路徑
        
    except Exception as e:
        print(f"發生錯誤: {e}")
        return None

if __name__ == "__main__":
    mp4_path = input("請輸入 MP4 檔案路徑: ")
    convert_mp4_to_mp3(mp4_path)
