from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# 初始化 Ollama Embeddings (使用 llama3 模型)
embeddings = OllamaEmbeddings(model="llama3")

# 範例資料
documents = [
    Document(page_content="台灣是亞洲一個美麗的島嶼，以美食和友善的人民聞名。"),
    Document(page_content="日本以其傳統文化和現代科技並存的獨特風貌聞名於世。"),
    Document(page_content="美國擁有多樣化的文化和風景，並以科技發展和創新著稱。"),
    Document(page_content="法國以其美食、時尚和藝術聞名，是歐洲旅遊熱門目的地。"),
]

# 建立向量資料庫
db = FAISS.from_documents(documents, embeddings)

# 測試查詢
query = "有哪些國家以美食聞名？"
result = db.similarity_search(query, k=2)

# 顯示結果
print("🔍 查詢結果：")
for i, doc in enumerate(result):
    print(f"{i + 1}. {doc.page_content}")

# # 使用 similarity_search_with_score() 來取得相似度分數
# results = db.similarity_search_with_score(query, k=2)

# # 顯示結果 (按相似度排序)
# print("🔍 查詢結果 (包含相似度分數)：")
# for i, (doc, score) in enumerate(sorted(results, key=lambda x: x[1], reverse=True), 1):
#     print(f"{i}. {doc.page_content} (相似度: {score:.4f})")