import json
import re

def generate_glm4_format(input_srt_file, output_json_file):
    def parse_subtitles(subtitle_text):
        messages = []
        current_message = []
        speaker_mapping = {}
        usertag = "user"
        AItag = "assistant"
        roletag = "role"
        contenttag = "content"
        conversationtag = "messages"

        lines = subtitle_text.strip().split("\n")
        prev_speaker = None
        assigned_speakers = 0  # 用於確認前兩組對話的 Speaker

        for line in lines:
            if re.match(r'\d+', line) or '-->' in line:
                continue

            match = re.match(r'(Speaker \d+):(.+)', line)
            if match:
                speaker, text = match.groups()

                # 設定前兩個出現的 Speaker，確保 Speaker 0 / 1 定義
                if speaker not in speaker_mapping and assigned_speakers < 2:
                    speaker_mapping[speaker] = usertag if assigned_speakers == 0 else AItag
                    assigned_speakers += 1

                speaker_role = speaker_mapping.get(speaker, AItag)  # 預設未出現的當 assistant

                if prev_speaker and prev_speaker != speaker_role:
                    messages.append({roletag: prev_speaker, contenttag: "，".join(current_message).strip() + "。"})
                    current_message = []

                current_message.append(text.strip())
                prev_speaker = speaker_role
            else:
                if current_message:
                    current_message.append(line.strip())

        if current_message:
            messages.append({roletag: prev_speaker, contenttag: "，".join(current_message).strip() + "。"})

        return {conversationtag: messages}

    with open(input_srt_file, "r", encoding="utf-8") as file:
        subtitle_text = file.read()

    data = parse_subtitles(subtitle_text)

    with open(output_json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"JSON 文件已成功寫入 {output_json_file}")

