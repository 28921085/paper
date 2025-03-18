from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from rag_database import DatabaseManager

embeddings = OllamaEmbeddings(model="llama3")
DB_PATH = "Jim"

# # 初始資料
# initial_documents = [
#     Document(page_content="台灣是亞洲一個美麗的島嶼，以美食和友善的人民聞名。"),
#     Document(page_content="日本以其傳統文化和現代科技並存的獨特風貌聞名於世。"),
#     Document(page_content="美國擁有多樣化的文化和風景，並以科技發展和創新著稱。"),
#     Document(page_content="法國以其美食、時尚和藝術聞名，是歐洲旅遊熱門目的地。"),
# ]

# 初始化資料庫
# db_manager = DatabaseManager(DB_PATH, embeddings, initial_documents)
db_manager = DatabaseManager(DB_PATH, embeddings)


# 測試查詢
db_manager.search_data("Jim對擇偶有什麼條件",10)


# # 測試更新
# update_data(db, "台灣是亞洲一個美麗的島嶼，以美食和友善的人民聞名。", "台灣擁有豐富的夜市文化，吸引許多觀光客。", DB_PATH)  
# search_data(db, "台灣")  

# # 測試刪除
# db = delete_data(db, "日本以其傳統文化和現代科技並存的獨特風貌聞名於世。", DB_PATH)  
# search_data(db, "日本")  


# # 使用 similarity_search_with_score() 來取得相似度分數
# results = db.similarity_search_with_score(query, k=2)

# # 顯示結果 (按相似度排序)
# print("🔍 查詢結果 (包含相似度分數)：")
# for i, (doc, score) in enumerate(sorted(results, key=lambda x: x[1], reverse=True), 1):
#     print(f"{i}. {doc.page_content} (相似度: {score:.4f})")