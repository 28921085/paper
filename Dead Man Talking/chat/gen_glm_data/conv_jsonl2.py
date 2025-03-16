import json

# 讀取 JSON 檔案
filename='jim-7'
file_path = f"{filename}.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 轉換成符合要求的 JSONL 格式

output_file_path= f"{filename}.jsonl"

with open(output_file_path, "w", encoding="utf-8") as jsonl_file:
    for conversation in data:
        jsonl_entry = {"messages": conversation["messages"]}
        jsonl_file.write(json.dumps(jsonl_entry, ensure_ascii=False) + "\n")


print(output_file_path)