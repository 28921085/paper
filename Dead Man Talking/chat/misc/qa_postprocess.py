from pathlib import Path

# 讀取原始檔案
input_path = Path("qa_record.txt")  # 可改為實際檔案路徑
with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 處理 QA 對：保留 model 後的回答
processed_qa = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("Q:"):
        question = line
        answer_lines = []
        i += 1
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("Q:"):
                break
            if line == "model":
                i += 1
                if i < len(lines):
                    answer_lines.append("A: " + lines[i].strip())
                break
            i += 1
        processed_qa.append(question)
        if answer_lines:
            processed_qa.extend(answer_lines)
    else:
        i += 1

# 插入空白行分隔 QA 對
formatted_qa = []
i = 0
while i < len(processed_qa):
    formatted_qa.append(processed_qa[i])  # Q:
    if i + 1 < len(processed_qa) and processed_qa[i + 1].startswith("A:"):
        formatted_qa.append(processed_qa[i + 1])  # A:
        formatted_qa.append("")  # 空白行
        i += 2
    else:
        i += 1

# 寫入處理後檔案
output_path = Path("qa_record_cleaned_spaced.txt")  # 可改為你要的儲存路徑
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(formatted_qa))

print(f"已儲存處理後的檔案：{output_path}")
