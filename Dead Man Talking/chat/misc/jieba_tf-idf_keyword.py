import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

# 讀取整份 law.txt
with open("law.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# 修正：支援 xxxx 條 / xxxx-x 條
pattern = r"(第\s*\d+(?:-\d+)?\s*條)\s*\n?(.+?)(?=(第\s*\d+(?:-\d+)?\s*條|$))"
matches = re.findall(pattern, raw_text, re.DOTALL)

# law_paragraphs: 儲存每條法條的完整內文
law_paragraphs = [f"{m[0]}\n{m[1].strip()}" for m in matches]

# jieba 斷詞（可加入自訂詞典）
tokenized_docs = [" ".join(jieba.lcut(para)) for para in law_paragraphs]

# 計算 TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(tokenized_docs)
feature_names = vectorizer.get_feature_names_out()

# 顯示每條法條的 top K 關鍵詞
top_k = 10
with open("keyword_info.txt", "w", encoding="utf-8") as f:
    for i, row in enumerate(tfidf_matrix.toarray()):
        # 法條標題（如：第 1080 條）
        title = law_paragraphs[i].splitlines()[0]
        f.write(f"\n📄 {title} 關鍵字：\n")
        
        # 取得 top K 關鍵詞的索引
        top_indices = row.argsort()[-top_k:][::-1]
        for idx in top_indices:
            score = row[idx]
            if score > 0:
                f.write(f"  {feature_names[idx]}: {score:.4f}\n")
