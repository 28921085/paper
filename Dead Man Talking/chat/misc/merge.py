import json
import re
from collections import Counter

def parse_emotion_format(data):
    parsed = []
    for line in data.strip().split("\n"):
        match = re.match(r"Time: ([\d.]+) sec, Emotion: (\w+)", line)
        if match:
            time = float(match.group(1))
            emotion = match.group(2)
            parsed.append({"time": time, "emotion": emotion})
    return parsed

def parse_text_format(data):
    parsed = []
    lines = data.strip().split("\n")
    for i in range(len(lines)):
        if re.match(r"^\d+$", lines[i]):
            text_match = re.search(r"-->", lines[i+1])
            if text_match and i+2 < len(lines):
                text = lines[i+2].strip()
                if text:
                    start_time = re.search(r"(\d+:\d+:\d+,\d+)", lines[i+1])
                    if start_time:
                        time_parts = start_time.group(1).replace(",", ".").split(":")
                        start_time_sec = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + float(time_parts[2])
                        parsed.append({"time": start_time_sec, "text": text})
    return parsed

def merge_data(emotion_data, text_data, offset=0):
    aggregated = {}
    text_data = [{"time": item["time"] + offset, "text": item["text"]} for item in text_data]

    for item1 in emotion_data:
        closest_item2 = min(text_data, key=lambda x: abs(x["time"] - item1["time"]))
        if abs(closest_item2["time"] - item1["time"]) <= 1.0:  # Adjust threshold as needed
            text = closest_item2["text"]
            emotion = item1["emotion"]
            if text not in aggregated:
                aggregated[text] = Counter()
            aggregated[text][emotion] += 1

    # 保留每句話中出現次數最高的情緒
    merged = []
    for text, emotion_counts in aggregated.items():
        most_common_emotion = emotion_counts.most_common(1)[0][0]
        merged.append({"text": text, "emotion": most_common_emotion})

    return merged

# 讀取檔案
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# 輸入檔案路徑
emotion_file = "video.txt"
text_file = "text.srt"

# Offset 設定
offset = -(8*60+4)  # 假設影片需要對齊的秒數

# 從檔案讀取資料
emotion_content = read_file(emotion_file)
text_content = read_file(text_file)

# 資料處理
emotion_parsed = parse_emotion_format(emotion_content)
text_parsed = parse_text_format(text_content)
merged_data = merge_data(emotion_parsed, text_parsed, offset=offset)

# 儲存為 ChatGLM 格式
output_file = "chatglm_formatted.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"資料已成功轉換並儲存為 {output_file}")
