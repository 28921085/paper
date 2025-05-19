from sentence_transformers import SentenceTransformer, util
import torch

# 初始化模型
model = SentenceTransformer('shibing624/text2vec-base-chinese')

def extract_answers(file_path):
    answers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("A:"):
                answer = line[2:].strip()
                if answer:  # 忽略空的 A:
                    answers.append(answer)
    return answers

# 讀取 QA 對應答案
qa_ex_answers = extract_answers("qa_ex.txt")
qa_record_answers = extract_answers("qa_record.txt")
print(len(qa_ex_answers))
print(len(qa_record_answers))
# 檢查數量是否一致
min_len = min(len(qa_ex_answers), len(qa_record_answers))
qa_ex_answers = qa_ex_answers[:min_len]
qa_record_answers = qa_record_answers[:min_len]

# 比對並記錄餘弦相似度
results = []
cos_sims = []

for ref, out in zip(qa_ex_answers, qa_record_answers):
    emb_ref = model.encode(ref, convert_to_tensor=True)
    emb_out = model.encode(out, convert_to_tensor=True)
    cosine_sim = util.cos_sim(emb_ref, emb_out).item()
    cos_sims.append(cosine_sim)

    result_entry = f"資料集答案: {ref}\n模型輸出: {out}\nCosine Similarity: {cosine_sim:.4f}\n"
    results.append(result_entry)

# 寫入結果檔案
with open("cos_result.txt", "w", encoding="utf-8") as f:
    for entry in results:
        f.write(entry + "\n")

# 計算並輸出平均相似度
avg_similarity = sum(cos_sims) / len(cos_sims)
print(f"平均語意相似度：{avg_similarity:.4f}")



# from sentence_transformers import SentenceTransformer, util

# # 使用支援中文的預訓練模型（你也可以換成 huggingface 上的其他模型）
# model = SentenceTransformer('shibing624/text2vec-base-chinese')

# # 範例句子
# reference_answer = "根據民法第184條，侵權行為需具備故意或過失。"
# model_output = "依據民法第184條，若行為人有過失，也須負侵權責任。"

# # 編碼成 contextual embeddings（768維向量）
# embedding_ref = model.encode(reference_answer, convert_to_tensor=True)
# embedding_output = model.encode(model_output, convert_to_tensor=True)

# # 計算餘弦相似度
# cosine_sim = util.cos_sim(embedding_ref, embedding_output)

# print(f"模型輸出與參考答案的語意相似度：{cosine_sim.item():.4f}")
