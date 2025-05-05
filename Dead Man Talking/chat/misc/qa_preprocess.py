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
            if '問句:' in line:
                question = clean_text(re.sub(r'^.*?問句:\s*', '', line))
            elif '答句:' in line:
                answer = clean_text(re.sub(r'^.*?答句:\s*', '', line))

            if question and answer:
                qa_pairs.append({'question': question, 'answer': answer})
                question = None
                answer = None

    return qa_pairs

# 主程式
if __name__ == "__main__":
    input_file = 'qa2.txt'
    output_file = 'qa_ex.jsonl'

    qa_results = extract_qas_from_txt(input_file)

    with open(output_file, 'w', encoding='utf-8') as f:
        for qa in qa_results:
            json.dump(qa, f, ensure_ascii=False)
            f.write('\n')

    print(f"✅ 共寫入 {len(qa_results)} 筆問答對到 {output_file}")
