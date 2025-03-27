from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import torch
from transformers import AutoTokenizer, AutoModel
from rag_database import DatabaseManager, CustomEmbedding
# embeddings = OllamaEmbeddings(model="llama3")
# # DB_PATH = "Jim"
# DB_PATH = "Law"

# # 初始資料
# initial_documents = [
#     Document(page_content="台灣是亞洲一個美麗的島嶼，以美食和友善的人民聞名。"),
#     Document(page_content="日本以其傳統文化和現代科技並存的獨特風貌聞名於世。"),
#     Document(page_content="美國擁有多樣化的文化和風景，並以科技發展和創新著稱。"),
#     Document(page_content="法國以其美食、時尚和藝術聞名，是歐洲旅遊熱門目的地。"),
# ]

# 初始化資料庫
# db_manager = DatabaseManager(DB_PATH, embeddings, initial_documents)
# db_manager = DatabaseManager(DB_PATH, embeddings)


# # 測試查詢
# db_manager.search_data("無行為能力",5)
# db_manager.search_data("Jim對擇偶有什麼條件",10)

DB_PATH = "Law"
# DB_PATH = "Jim"
# GPU 裝置檢查
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



# 初始化模型
tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-base').half().to(device)

# 初始化 Embedding 類別
embedding_model = CustomEmbedding(model, tokenizer, device)
# 初始化資料庫
db_manager = DatabaseManager(DB_PATH, embedding_model)
db_manager.search_data("失蹤", 5)