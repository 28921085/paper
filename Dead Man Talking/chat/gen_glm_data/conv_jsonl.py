import json

def convert_json_to_jsonl(input_json_file, output_jsonl_file):
    with open(input_json_file, 'r', encoding='utf-8') as file:
        input_data = json.load(file)

    messages = input_data["messages"]
    paired_messages = []

    for i in range(0, len(messages) - 1, 2):
        if messages[i]["role"] == "user" and messages[i+1]["role"] == "assistant":
            paired_messages.append({"messages": [messages[i], messages[i+1]]})

    with open(output_jsonl_file, 'w', encoding='utf-8') as f:
        for pair in paired_messages:
            json.dump(pair, f, ensure_ascii=False)
            f.write('\n')

    print(f"轉換完成，已儲存為 {output_jsonl_file}")
