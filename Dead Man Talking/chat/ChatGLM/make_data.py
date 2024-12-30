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
    pattern = r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(Speaker \d+:)?(.+?)(?=\n\n|\Z)"
    matches = re.findall(pattern, subtitle_text, re.DOTALL)
    subtitles = []
    for match in matches:
        idx, start, end, speaker, text = match
        text = text.replace('\n', ' ').strip()
        speaker = speaker.strip() if speaker else "Unknown"  # 如果沒有說話者，設為 "Unknown"
        if speaker.startswith("Speaker "):
            speaker = speaker.replace("Speaker ", "").replace(":", "")
        subtitles.append({
            "index": int(idx),
            "start": parse_time(start),
            "end": parse_time(end),
            "speaker": speaker,
            "text": text
        })
    return subtitles

# 拆分 Whisper 字幕為字級別的結構
def split_whisper_to_characters(whisper_subtitles):
    char_speaker_map = []
    for sub in whisper_subtitles:
        for char in sub["text"]:
            if re.match(r"\w", char):  # 只處理非標點符號的字符
                char_speaker_map.append({
                    "char": char,
                    "speaker": sub["speaker"],
                    "start": sub["start"],
                    "end": sub["end"]
                })
    return char_speaker_map

# 判斷區間是否重疊
def is_overlapping(start1, end1, start2, end2):
    return not (end1 < start2 or end2 < start1)

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
    char_speaker_map = split_whisper_to_characters(whisper_subtitles)
    cnt=0
    for correct_sub in correct_subtitles:
        speaker_count = Counter()
        correct_characters = [char for char in correct_sub["text"] if re.match(r"\w", char)]  # 過濾標點符號

        # 遍歷每個字並計算說話者
        for char in correct_characters:
            for i, char_speaker in enumerate(char_speaker_map):
                # 檢查字符和時間區間是否匹配
                if (char == char_speaker["char"] and
                        is_overlapping(correct_sub["start"], correct_sub["end"], char_speaker["start"], char_speaker["end"])):
                    speaker_count[char_speaker["speaker"]] += 1
                    # 移除已匹配的字符，避免重複計算
                    char_speaker_map.pop(i)
                    break

        # 印出計數資訊
        if cnt<100:
            print(f"正確字幕: {correct_sub['text']} 計數: {dict(speaker_count)}")
        cnt+=1
        # 忽略計數中的 "Unknown"
        if "Unknown" in speaker_count:
            del speaker_count["Unknown"]

        # 確定最可能的說話者
        if speaker_count:
            most_common_speaker = speaker_count.most_common(1)[0][0]
        else:
            # 如果無法確定說話者，使用正確字幕的說話者
            most_common_speaker = correct_sub.get("speaker", "Unknown")

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
        output.append(f"{idx}\n{format_time(sub['start'])} --> {format_time(sub['end'])}\nSpeaker {sub['speaker']}:{sub['text']}")
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
aligned = align_and_merge(correct_subtitles, whisper_subtitles)
merged = merge_speaker_subtitles(aligned)
result = output_merged_subtitles(merged)

with open("output.txt", "w", encoding="utf-8") as output_file:
    output_file.write(result)
