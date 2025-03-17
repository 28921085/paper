from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os

# 初始化 Ollama Embeddings (使用 llama3 模型)
embeddings = OllamaEmbeddings(model="llama3")

# 檢查資料庫是否已存在
DB_PATH = "Database"

# 🔹 初始資料
documents = [
    Document(page_content="台灣是亞洲一個美麗的島嶼，以美食和友善的人民聞名。"),
    Document(page_content="日本以其傳統文化和現代科技並存的獨特風貌聞名於世。"),
    Document(page_content="美國擁有多樣化的文化和風景，並以科技發展和創新著稱。"),
    Document(page_content="法國以其美食、時尚和藝術聞名，是歐洲旅遊熱門目的地。"),
]

# 🔹 建立或載入資料庫
def load_or_create_db(db_path, documents):
    if os.path.exists(db_path):
        db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
        print("✅ 已加載現有資料庫")
    else:
        db = FAISS.from_documents(documents, embeddings)
        db.save_local(db_path)
        print("✅ 已建立並儲存資料庫")
    return db

# 🔹 查詢資料 (Search)
def search_data(db, query, k=2):
    result = db.similarity_search(query, k=k)
    print("\n🔍 查詢結果：")
    for i, doc in enumerate(result):
        print(f"{i + 1}. {doc.page_content}")

# 🔹 新增資料 (Add)
def add_data(db, new_texts, db_path):
    new_docs = [Document(page_content=text) for text in new_texts]
    db.add_documents(new_docs)
    db.save_local(db_path)
    print("✅ 資料已成功新增")

# 🔹 刪除資料 (Delete)
def delete_data(db, delete_text, db_path):
    all_texts = [doc.page_content for doc in db.similarity_search("", k=100)]
    filtered_texts = [text for text in all_texts if text != delete_text]

    db = FAISS.from_documents([Document(page_content=text) for text in filtered_texts], embeddings)
    db.save_local(db_path)
    print(f"✅ 已成功刪除資料: {delete_text}")
    return db  # 更新後的 db 需返回以供後續使用

# 🔹 更新資料 (Update)
def update_data(db, old_text, new_text, db_path):
    db = delete_data(db, old_text, db_path)  # 先刪除舊資料
    add_data(db, [new_text], db_path)        # 再新增新資料
    print(f"✅ 已將資料 '{old_text}' 更新為 '{new_text}'")

# === 測試區 ===
db = load_or_create_db(DB_PATH, documents)

# 測試查詢
search_data(db, "亞洲的美麗島嶼")  

# 測試新增
add_data(db, ["德國以其精密工程和汽車工業聞名。"], DB_PATH)  
search_data(db, "汽車工業")  


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