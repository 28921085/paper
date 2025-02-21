import json

def convert_to_jsonl(input_json, output_file):
    messages = input_json["messages"]
    paired_messages = []

    # 將 user 和 assistant 對話配對
    for i in range(0, len(messages) - 1, 2):
        if messages[i]["role"] == "user" and messages[i+1]["role"] == "assistant":
            paired_messages.append({"messages": [messages[i], messages[i+1]]})

    # 寫入 JSONL 格式，每組對話獨立一行
    with open(output_file, 'w', encoding='utf-8') as f:
        for pair in paired_messages:
            json.dump(pair, f, ensure_ascii=False)
            f.write('\n')

filename = "output"
with open(f'{filename}.json', 'r', encoding='utf-8') as file:
    input_data = json.load(file)

# 指定輸出的 .jsonl 檔案名稱
output_filename = f"{filename}.jsonl"

# 轉換 JSON 至 JSONL
convert_to_jsonl(input_data, output_filename)

print(f"轉換完成，已儲存為 {output_filename}")
