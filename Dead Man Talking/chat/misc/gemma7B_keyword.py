# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import AutoTokenizer, AutoModel
import re
from tqdm import tqdm
from collections import Counter

tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b-it")
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-7b-it",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def extract_keywords(text,keywords):
    # 使用正則分段，每個 **關鍵字：** 開頭的區塊
    keyword_blocks = re.split(r"\*\*關鍵字：\*\*", text)

    for block in keyword_blocks:
        # 找出開頭為 * 或 - 的列，去除符號與空白
        lines = re.findall(r"[\*\-]\s*(.+)", block)
        for kw in lines:
            cleaned = kw.strip()
            if cleaned:
                keywords[cleaned]+=1
    
    return keywords

file_path = "law.txt"
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()
paragraphs = [line.strip() for line in text.strip().split("\n") if line.strip()]


# 假設 paragraphs 是你的條文段落清單
total = len(paragraphs)
keywords = Counter()
multipara = ""
cnt = 0

# tqdm 進度條初始化
pbar = tqdm(total=total, desc="擷取關鍵字中", ncols=80)

for i, para in enumerate(paragraphs):
    multipara += para
    cnt += 1

    if cnt == 20:
        cnt = 0
        input_text = (
            f"請閱讀以下法律條文片段後來擷取出可以做為常見法律問題問答的關鍵字，每個關鍵字不超過5個中文字，且盡量避免意義重複關鍵字。法律條文:{multipara}"
        )

        input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
        outputs = model.generate(**input_ids, max_new_tokens=1024)
        generated_ids = outputs[0][input_ids['input_ids'].shape[1]:]
        output_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

        extract_keywords(output_text, keywords)

        multipara = ""

    pbar.update(1)

pbar.close()

input_text=f"請閱讀以下法律條文片段後來擷取出可以做為常見法律問題問答的關鍵字，每個關鍵字不超過5個中文字，且盡量避免意義重複關鍵字。法律條文:{multipara}"


input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
outputs = model.generate(**input_ids, max_new_tokens=1024)
# 只取生成的部分（排除 prompt 長度的部分）
generated_ids = outputs[0][input_ids['input_ids'].shape[1]:]
output_text=tokenizer.decode(generated_ids, skip_special_tokens=True)
# print(tokenizer.decode(generated_ids, skip_special_tokens=True))
extract_keywords(output_text,keywords)
print(len(keywords))
common_keywords=keywords.most_common(200)
with open("keyword.txt", "w", encoding="utf-8") as f:
    for word, count in common_keywords:
        f.write(f"{word}\t{count}\n")