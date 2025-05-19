import re
import json

def clean_text(text):
    # 去除前後空白與 ** 符號
    cleaned = text.strip().lstrip('*').rstrip('*').strip()
    # 去除前後括號（包含全形與半形）
    cleaned = re.sub(r'^[（(]\s*(.*?)\s*[）)]$', r'\1', cleaned)
    return cleaned

def extract_qas_from_txt(file_path):
    qa_pairs = []
    question = None
    answer = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if 'Question:' in line:
                question = clean_text(re.sub(r'^.*?Question:\s*', '', line))
            elif 'Answer:' in line:
                answer = clean_text(re.sub(r'^.*?Answer:\s*', '', line))

            if question and answer:
                qa_pairs.append({'question': question, 'answer': answer})
                question = None
                answer = None

    return qa_pairs

# 主程式
if __name__ == "__main__":
    input_file = 'qa_from_chunks.txt'
    output_jsonl = 'qa_ex_en.jsonl'
    output_txt = 'qa_ex_en.txt'

    qa_results = extract_qas_from_txt(input_file)

    # 寫入 JSONL 檔案
    with open(output_jsonl, 'w', encoding='utf-8') as f_json:
        for qa in qa_results:
            json.dump(qa, f_json, ensure_ascii=False)
            f_json.write('\n')

    # 寫入 TXT 檔案（人類可讀格式）
    with open(output_txt, 'w', encoding='utf-8') as f_txt:
        for qa in qa_results:
            f_txt.write(f"Question: {qa['question']}\n")
            f_txt.write(f"Answer: {qa['answer']}\n\n")

    print(f"✅ 共寫入 {len(qa_results)} 筆問答對到：")
    print(f"📄 JSONL：{output_jsonl}")
    print(f"📄 TXT：{output_txt}")
