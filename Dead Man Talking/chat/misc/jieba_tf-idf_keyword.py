import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 1: 讀取全文
with open("law.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Step 2: 使用 jieba 斷詞（整份一次處理）
tokenized_text = " ".join(jieba.lcut(raw_text))

# Step 3: TF-IDF（只分析一份「整體文件」）
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([tokenized_text])
feature_names = vectorizer.get_feature_names_out()
tfidf_scores = tfidf_matrix.toarray()[0]  # 只有一份文件

# Step 4: 取 top k 關鍵字
top_k = 50
top_indices = tfidf_scores.argsort()[-top_k:][::-1]

# Step 5: 寫入檔案
with open("keyword_info.txt", "w", encoding="utf-8") as f:
    f.write("📄 全文前 Top {} 關鍵字：\n".format(top_k))
    for idx in top_indices:
        score = tfidf_scores[idx]
        f.write(f"  {feature_names[idx]}: {score:.4f}\n")
