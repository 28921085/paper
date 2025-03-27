from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
import torch.nn.functional as F
import os
import torch
from torch import Tensor

class DatabaseManager:
    def __init__(self, db_path, embeddings, initial_documents=None):
        self.db_path = db_path
        self.embeddings = embeddings
        self.db = self._load_or_create_db(initial_documents or [])

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
        resultText = ""
        for i, doc in enumerate(result):
            print(f"{i + 1}. {doc.page_content}")
            resultText += f'[{doc.page_content}],' 
        return resultText

    def add_data(self, new_texts):
        new_docs = [Document(page_content=text.strip()) for text in new_texts]
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

# Average pooling function
def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

# 自訂 Embedding 類別 class
class CustomEmbedding(Embeddings):
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def embed_documents(self, texts):
        embeddings_list = []
        batch_size = 8  # 控制記憶體使用
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]

            batch_dict = self.tokenizer(batch_texts, max_length=512, padding=True, truncation=True, return_tensors='pt').to(self.device)
            with torch.no_grad():  # 禁用梯度以降低記憶體消耗
                outputs = self.model(**batch_dict)

            embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
            embeddings = F.normalize(embeddings, p=2, dim=1).cpu()
            embeddings_list.append(embeddings)
            print(f'{i}/{len(texts)}')

        return torch.cat(embeddings_list, dim=0).tolist()  # FAISS 需要 List 格式

    def embed_query(self, text):
        return self.embed_documents([text])[0]
