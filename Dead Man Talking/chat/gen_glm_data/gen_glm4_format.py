import json
import re

def generate_glm4_format(input_srt_file, output_json_file, ai_speaker="Speaker 0"):
    def parse_subtitles(subtitle_text):
        messages = []
        current_message = []
        usertag = "user"
        AItag = "assistant"
        roletag = "role"
        contenttag = "content"
        conversationtag = "messages"

        lines = subtitle_text.strip().split("\n")
        prev_speaker = None

        for line in lines:
            if re.match(r'^\d+$', line) or '-->' in line:  # 跳過字幕編號和時間戳
                continue

            match = re.match(r'(Speaker \d+):(.+)', line)
            if match:
                speaker, text = match.groups()
                speaker_role = AItag if speaker == ai_speaker else usertag  # 指定 AI 角色，其他皆為 user

                if prev_speaker is not None and prev_speaker != speaker_role:
                    # 角色變更時，將先前對話存入
                    messages.append({roletag: prev_speaker, contenttag: "，".join(current_message).strip() + "。"})
                    current_message = []

                current_message.append(text.strip())
                prev_speaker = speaker_role
            else:
                if current_message:
                    current_message.append(line.strip())

        # 處理最後一組對話
        if current_message:
            messages.append({roletag: prev_speaker, contenttag: "，".join(current_message).strip() + "。"})

        return {conversationtag: messages}

    with open(input_srt_file, "r", encoding="utf-8") as file:
        subtitle_text = file.read()

    data = parse_subtitles(subtitle_text)

    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"JSON 文件已成功寫入 {output_json_file}")
