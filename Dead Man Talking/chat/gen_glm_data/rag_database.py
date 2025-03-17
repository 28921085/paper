from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os

class DatabaseManager:
    def __init__(self, db_path, embeddings, initial_documents=None):
        self.db_path = db_path
        self.embeddings = embeddings
        self.db = self._load_or_create_db(initial_documents or [])  # 初始資料集不可為空

    def _load_or_create_db(self, documents):
        if os.path.exists(self.db_path):
            db = FAISS.load_local(self.db_path, self.embeddings, allow_dangerous_deserialization=True)
            print("✅ 已加載現有資料庫")
        else:
            if not documents:
                raise ValueError("❌ 無法建立資料庫：初始資料為空")
            db = FAISS.from_documents(documents, self.embeddings)
            db.save_local(self.db_path)
            print("✅ 已建立並儲存資料庫")
        return db

    def search_data(self, query, k=2):
        result = self.db.similarity_search(query, k=k)
        print("\n🔍 查詢結果：")
        for i, doc in enumerate(result):
            print(f"{i + 1}. {doc.page_content}")

    def add_data(self, new_texts):
        new_docs = [Document(page_content=text) for text in new_texts]
        self.db.add_documents(new_docs)
        self.db.save_local(self.db_path)
        print("✅ 資料已成功新增")

    def delete_data(self, delete_text):
        all_texts = [doc.page_content for doc in self.db.similarity_search("", k=100)]
        filtered_texts = [text for text in all_texts if text != delete_text]

        self.db = FAISS.from_documents([Document(page_content=text) for text in filtered_texts], self.embeddings)
        self.db.save_local(self.db_path)
        print(f"✅ 已成功刪除資料: {delete_text}")

    def update_data(self, old_text, new_text):
        self.delete_data(old_text)
        self.add_data([new_text])
        print(f"✅ 已將資料 '{old_text}' 更新為 '{new_text}'")