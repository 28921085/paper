import json

def convert_to_glm4_format(input_file, output_file):
    conversations = []
    messages = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            if messages:
                conversations.append({"messages": messages})
                messages = []
            continue
        
        if line.startswith("user:"):
            messages.append({"role": "user", "content": line.replace("user:", "").strip()})
        elif line.startswith("assistant:"):
            messages.append({"role": "assistant", "content": line.replace("assistant:", "").strip()})
    
    if messages:
        conversations.append({"messages": messages})
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)
    
    print(f"Converted conversation saved to {output_file}")

# 請替換為你的檔案名稱
filename='jim-7'
input_file = f"{filename}_output.txt"  # 你的原始對話檔案
output_file = f"{filename}.json"  # 轉換後的 JSON 檔案

convert_to_glm4_format(input_file, output_file)