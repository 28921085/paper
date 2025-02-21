import os
import json
import random

# 設定資料夾名稱及輸出檔案名稱
raw_data_dir = "raw data"
output_files = {
    "train": "train.jsonl",
    "test": "test.jsonl",
    "val": "val.jsonl"
}

# 讀取所有 jsonl 檔案內容
all_data = []
for filename in os.listdir(raw_data_dir):
    if filename.endswith(".jsonl"):
        file_path = os.path.join(raw_data_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            all_data.extend(f.readlines())

# 總行數
total_lines = len(all_data)
print(f"Total lines: {total_lines}")

# 打亂資料順序，確保隨機性
random.shuffle(all_data)

# 計算切割比例
train_size = int(total_lines * 0.6)
test_size = int(total_lines * 0.2)
val_size = total_lines - train_size - test_size

# 切割資料
data_splits = {
    "train": all_data[:train_size],
    "test": all_data[train_size:train_size + test_size],
    "val": all_data[train_size + test_size:]
}

# 寫入到對應的檔案
for split, data in data_splits.items():
    with open(output_files[split], "w", encoding="utf-8") as f:
        f.writelines(data)
    print(f"{split}.jsonl saved with {len(data)} lines.")
