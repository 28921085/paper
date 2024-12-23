import whisper
import os
# 載入 Whisper 模型
model = whisper.load_model("base")
path=os.path.abspath("target.mp3")
print(path)
# 轉錄音訊檔案
result = model.transcribe(path)


# 取得轉錄的文字及時間戳記
segments = result.get("segments", [])

# 將結果寫入 output.txt
with open("output.txt", "w", encoding="utf-8") as file:
    for segment in segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        # 格式化輸出
        line = f"[{start_time:.2f} - {end_time:.2f}] {text}\n"
        file.write(line)

print("轉錄完成，結果已寫入 output.txt！")
