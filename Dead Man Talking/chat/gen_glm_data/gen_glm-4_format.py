import json
import re

def parse_subtitles(subtitle_text):
    messages = []
    current_message = []
    usertag="user"
    AItag="assistant"
    roletag="role"
    contenttag="content"
    conversationtag="messages"

    # usertag="human"
    # AItag="gpt"
    # roletag="from"
    # contenttag="value"
    # conversationtag="conversations"
    
    lines = subtitle_text.strip().split("\n")
    prev_speaker = None
    
    for line in lines:
        # 跳過時間戳與索引數字
        if re.match(r'\d+', line) or '-->' in line:
            continue
        
        match = re.match(r'(Speaker \d+):(.+)', line)
        if match:
            speaker, text = match.groups()
            speaker_role = usertag if speaker == "Speaker 1" else AItag
            
            if prev_speaker and prev_speaker != speaker_role:
                # Speaker 改變，存儲當前對話
                messages.append({roletag: prev_speaker, contenttag: "，".join(current_message).strip() + "。"})
                current_message = []
            
            current_message.append(text.strip())
            prev_speaker = speaker_role
        else:
            # 如果沒有匹配到 Speaker，那就是上一條對話的延續
            if current_message:
                current_message.append(line.strip())
    
    # 添加最後一條對話
    if current_message:
        messages.append({roletag: prev_speaker, contenttag: "，".join(current_message).strip() + "。"})
    
    # return [{conversationtag : messages}] #llamaFactory
    return {conversationtag : messages}

# 讀取輸入文件
with open("output_modify.txt", "r", encoding="utf-8") as file:
    subtitle_text = file.read()

# 轉換格式
data = parse_subtitles(subtitle_text)

# 輸出 JSON 檔案
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON 文件已成功寫入 output.json")
