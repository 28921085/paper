import json

def convert_to_jsonl(input_json, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        messages = input_json["messages"]
        for i in range(0, len(messages) - 1, 2):
            if messages[i]["role"] == "user" and messages[i + 1]["role"] == "assistant":
                entry = {
                    "content": messages[i]["content"],
                    "summary": messages[i + 1]["content"]
                }
                json.dump(entry, f, ensure_ascii=False)
                f.write('\n')
filename="val"
# 輸入的 JSON 格式數據
with open(f'{filename}.json', 'r', encoding='utf-8') as file:
    input_data = json.load(file)

# 指定輸出的 .jsonl 檔案名稱
output_filename = f"{filename}.jsonl"

# 轉換 JSON 至 JSONL
convert_to_jsonl(input_data, output_filename)

print(f"轉換完成，已儲存為 {output_filename}")
