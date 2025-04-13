from collections import Counter
import re

# 讀取法律條文
with open("law.txt", "r", encoding="utf-8") as f:
    law_text = f.read()

# 提取可能的關鍵詞：只考慮 2-5 字詞，過濾重複與空白，統計出現頻率
phrases = re.findall(r'[\u4e00-\u9fa5]{2,5}', law_text)
filtered = [p for p in phrases if len(set(p)) > 1]  # 去除重複字元組成的關鍵詞（如「日日」）
counter = Counter(filtered)
common_phrases = counter.most_common(200)  # 先取前 200 多次出現的詞進行過濾
# 移除意義重複（語義相近字開頭的詞），例如「意思表示」「表示意思」→保留一個
unique_keywords = []
seen_stems = set()

for phrase, _ in common_phrases:
    if any(stem in phrase for stem in seen_stems):
        continue
    unique_keywords.append(phrase)
    seen_stems.add(phrase[:2])  # 根據前2字過濾相近詞語

unique_keywords = unique_keywords[:200]  
with open("keyword.txt", "w", encoding="utf-8") as f:
    for word in unique_keywords:
        f.write(f"{word}\n")
