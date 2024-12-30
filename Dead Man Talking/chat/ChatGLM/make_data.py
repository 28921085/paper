import re
from datetime import timedelta
from collections import Counter

# 將字幕時間戳轉換為 timedelta
def parse_time(timestamp):
    h, m, s = map(float, timestamp.replace(',', '.').split(':'))
    return timedelta(hours=h, minutes=m, seconds=s)

# 將 timedelta 轉回字幕時間戳格式
def format_time(td):
    total_seconds = int(td.total_seconds())
    ms = int((td.total_seconds() - total_seconds) * 1000)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

# 解析字幕檔案
def parse_subtitles(subtitle_text):
    pattern = r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+?)(?=\n\n|\Z)"
    matches = re.findall(pattern, subtitle_text, re.DOTALL)
    subtitles = []
    for match in matches:
        idx, start, end, text = match
        text = text.replace('\n', ' ').strip()
        subtitles.append({
            "index": int(idx),
            "start": parse_time(start),
            "end": parse_time(end),
            "text": text
        })
    return subtitles

# 合併同一個說話者的字幕
def merge_speaker_subtitles(subtitles):
    merged = []
    buffer = {
        "start": None,
        "end": None,
        "speaker": None,
        "text": []
    }

    for sub in subtitles:
        if buffer["speaker"] == sub["speaker"]:
            buffer["end"] = sub["end"]
            buffer["text"].append(sub["text"])
        else:
            if buffer["speaker"] is not None:
                merged.append({
                    "start": buffer["start"],
                    "end": buffer["end"],
                    "speaker": buffer["speaker"],
                    "text": "\n".join(buffer["text"])
                })
            buffer = {
                "start": sub["start"],
                "end": sub["end"],
                "speaker": sub["speaker"],
                "text": [sub["text"]]
            }

    if buffer["speaker"] is not None:
        merged.append({
            "start": buffer["start"],
            "end": buffer["end"],
            "speaker": buffer["speaker"],
            "text": "\n".join(buffer["text"])
        })

    return merged

# 識別正確字幕與 Whisper 字幕並統計說話者

def align_and_merge(correct_subtitles, whisper_subtitles):
    aligned_subtitles = []
    whisper_idx = 0

    for correct_sub in correct_subtitles:
        speaker_count = Counter()
        while whisper_idx < len(whisper_subtitles):
            whisper_sub = whisper_subtitles[whisper_idx]
            
            # 如果 Whisper 的時間範圍包含正確字幕
            if (whisper_sub["start"] <= correct_sub["start"] <= whisper_sub["end"] or
                whisper_sub["start"] <= correct_sub["end"] <= whisper_sub["end"]):

                # 記錄該字幕的說話者
                speaker_count[whisper_sub["speaker"]] += 1

                # 移動到下一個 Whisper 字幕
                whisper_idx += 1
            else:
                break

        # 確定最可能的說話者
        most_common_speaker = speaker_count.most_common(1)[0][0] if speaker_count else None

        aligned_subtitles.append({
            "start": correct_sub["start"],
            "end": correct_sub["end"],
            "speaker": most_common_speaker,
            "text": correct_sub["text"]
        })

    return aligned_subtitles

# 合併與輸出結果

def output_merged_subtitles(merged_subtitles):
    output = []
    for idx, sub in enumerate(merged_subtitles, start=1):
        output.append(f"{idx}\n{format_time(sub['start'])} --> {format_time(sub['end'])}\nSpeaker {sub['speaker']}:\n{sub['text']}\n")
    return "\n".join(output)

# 從文件讀取字幕
def read_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 測試案例
correct_subtitle_text = read_srt_file("correct.srt")
whisper_subtitle_text = read_srt_file("whisper.srt")

correct_subtitles = parse_subtitles(correct_subtitle_text)
whisper_subtitles = parse_subtitles(whisper_subtitle_text)

print("字幕:",correct_subtitles)
print("whisper:",whisper_subtitles)
aligned = align_and_merge(correct_subtitles, whisper_subtitles)
merged = merge_speaker_subtitles(aligned)
result = output_merged_subtitles(merged)

with open("output.txt", "w", encoding="utf-8") as output_file:
    output_file.write(result)
