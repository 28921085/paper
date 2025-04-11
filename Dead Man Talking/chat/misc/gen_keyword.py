# 基本流程的Python實作，改為從 law.txt 讀取文本
import os
import numpy as np
import jieba
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# 檔案讀取
file_path = "law.txt"
if not os.path.exists(file_path):
    raise FileNotFoundError("找不到 law.txt 檔案，請確認檔案已放置在正確位置。")

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# 分段（以行分句）
paragraphs = [line.strip() for line in text.strip().split("\n") if line.strip()]
print("分段")
# 步驟1：使用 YAKE 抽關鍵詞（TF-IDF 或其他方法也可替代）
all_words = []

# 對每段條文進行分詞，收集所有詞彙
for para in paragraphs:
    words = jieba.lcut(para)
    # 過濾掉太短的詞（如一個字的詞）與標點
    all_words.extend([w for w in words if len(w) > 1 and w.isalnum()])

# 統計詞頻
word_freq = Counter(all_words)
print(len(word_freq))
# 取前 100 個最常出現的詞作為關鍵詞（你可以調整數量）
keyword_list = [word for word, freq in word_freq.most_common(2000)]
print("1：yake 抽關鍵詞")
# 步驟2：語意向量化
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(keyword_list, normalize_embeddings=True)
print("2：語意向量化")
# 步驟3：語意去重（用 Cosine 相似度過濾重複）
similarity_matrix = cosine_similarity(embeddings)
threshold = 0.85  # 語意重複閾值
print("3：語意去重（用 Cosine 相似度過濾重複）")
# 建立去重關鍵詞清單
filtered_keywords = []
for i, kw in enumerate(keyword_list):
    if all(cosine_similarity([embeddings[i]], [embeddings[j]])[0][0] < threshold for j in filtered_keywords):
        filtered_keywords.append(i)

deduplicated_keywords = [keyword_list[i] for i in filtered_keywords]
dedup_embeddings = embeddings[filtered_keywords]
print("建立去重關鍵詞清單")
# 步驟4：語意多樣性選擇（用 KMeans 抽不同語意類別）
n_clusters = min(30, len(dedup_embeddings))  # 最多選 30 個關鍵字（可自行調整）
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(dedup_embeddings)
cluster_centers = kmeans.cluster_centers_
print("4：語意多樣性選擇")
# 選每群中最靠近中心的詞作代表
final_keywords = []
for i in range(n_clusters):
    cluster_indices = np.where(kmeans.labels_ == i)[0]
    center = cluster_centers[i]
    closest_idx = cluster_indices[np.argmin(np.linalg.norm(dedup_embeddings[cluster_indices] - center, axis=1))]
    final_keywords.append(deduplicated_keywords[closest_idx])
print("選每群中最靠近中心的詞作代表")
# 儲存關鍵字清單成為 keyword.txt（每行一個關鍵字）
with open("keyword.txt", "w", encoding="utf-8") as f:
    for kw in final_keywords:
        f.write(kw + "\n")

print("✅ 關鍵字清單已儲存至 keyword.txt")