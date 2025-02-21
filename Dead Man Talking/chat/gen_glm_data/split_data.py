import json
import random
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
# 讀取原始 JSON 檔案
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# 儲存 JSON 檔案
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 將 human 和 gpt 兩兩成對
def pair_conversations(conversations):
    paired = []
    temp_pair = []
    for convo in conversations:
        temp_pair.append(convo)
        if convo[roletag] == AItag:
            paired.append(temp_pair)
            temp_pair = []
    return paired

# 隨機分割資料集
def split_data(data, train_ratio=0.6, val_ratio=0.2, test_ratio=0.2):
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "比例總和應為 1"
    
    conversations = data[conversationtag]
    paired_conversations = pair_conversations(conversations)
    random.shuffle(paired_conversations)  # 打亂順序
    
    total = len(paired_conversations)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_data = {conversationtag: [msg for pair in paired_conversations[:train_end] for msg in pair]}
    val_data = {conversationtag: [msg for pair in paired_conversations[train_end:val_end] for msg in pair]}
    test_data = {conversationtag: [msg for pair in paired_conversations[val_end:] for msg in pair]}
    
    return train_data, val_data, test_data

# 主函式
def main():
    input_filename = "output.json"  # 替換為你的檔案名稱
    
    data = load_json(input_filename)
    train_data, val_data, test_data = split_data(data)
    
    save_json(train_data, "train.json")
    save_json(val_data, "val.json")
    save_json(test_data, "test.json")
    
    print("資料分割完成，已儲存 train.json, val.json, test.json")

if __name__ == "__main__":
    main()
