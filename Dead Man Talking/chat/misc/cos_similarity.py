from sentence_transformers import SentenceTransformer, util

# 使用支援中文的預訓練模型（你也可以換成 huggingface 上的其他模型）
model = SentenceTransformer('shibing624/text2vec-base-chinese')

# 範例句子
reference_answer = "根據民法第184條，侵權行為需具備故意或過失。"
model_output = "依據民法第184條，若行為人有過失，也須負侵權責任。"

# 編碼成 contextual embeddings（768維向量）
embedding_ref = model.encode(reference_answer, convert_to_tensor=True)
embedding_output = model.encode(model_output, convert_to_tensor=True)

# 計算餘弦相似度
cosine_sim = util.cos_sim(embedding_ref, embedding_output)

print(f"模型輸出與參考答案的語意相似度：{cosine_sim.item():.4f}")
