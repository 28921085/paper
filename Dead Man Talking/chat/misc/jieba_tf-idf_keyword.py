import re
import jieba
import math
from sklearn.feature_extraction.text import TfidfVectorizer

# 讀取整份 law.txt
with open("law.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# 支援 xxxx 條 / xxxx-x 條
pattern = r"(第\s*\d+(?:-\d+)?\s*條)\s*\n?(.+?)(?=(第\s*\d+(?:-\d+)?\s*條|$))"
matches = re.findall(pattern, raw_text, re.DOTALL)

# law_paragraphs: 儲存每條法條的完整內文
law_paragraphs = [f"{m[0]}\n{m[1].strip()}" for m in matches]
print(len(law_paragraphs))

# 將每 group_size 條合併成一個段落
group_size = int(math.sqrt(len(law_paragraphs)))
grouped_paragraphs = [
    "\n".join(law_paragraphs[i:i+group_size])
    for i in range(0, len(law_paragraphs), group_size)
]

# jieba 斷詞處理
tokenized_groups = [" ".join(jieba.lcut(group)) for group in grouped_paragraphs]

# 計算 TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(tokenized_groups)
feature_names = vectorizer.get_feature_names_out()

# 🔍 統計每個關鍵字出現過的最高分數
keyword_max_score = {}

for row in tfidf_matrix.toarray():
    for idx, score in enumerate(row):
        if score > 0:
            word = feature_names[idx]
            if word not in keyword_max_score or score > keyword_max_score[word]:
                keyword_max_score[word] = score

# 🔢 排序並取前 200 名
top_keywords = sorted(keyword_max_score.items(), key=lambda x: x[1], reverse=True)[:200]

with open("keyword.txt", "w", encoding="utf-8") as f:
    # f.write("📊 前 200 個高 TF-IDF 關鍵字（取最大分數）：\n")
    for word, score in top_keywords:
        # f.write(f"{word}: {score:.4f}\n")
        f.write(f"{word}\n")

