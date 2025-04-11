import json

# 讀取 JSONL 檔案
filename='jim-7'
input_file = f"{filename}.jsonl"
output_file = f"{filename}.txt"

result = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)  # 解析 JSONL 每一行為一個 JSON 物件
        for message in entry["messages"]:
            result.append(f"{message['role']}: {message['content']}")

# 將結果寫入 output.txt
with open(output_file, "w", encoding="utf-8") as f:
    for line in result:
        f.write(line + "\n")

print(f"已成功將格式化內容寫入 {output_file}")
