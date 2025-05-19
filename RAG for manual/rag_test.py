import torch
from transformers import AutoTokenizer, AutoModel
from rag_database import DatabaseManager, CustomEmbedding


# DB_PATH = "Law"
DB_PATH = "Manual"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



# 初始化模型
tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-base').half().to(device)

# 初始化 Embedding 類別
embedding_model = CustomEmbedding(model, tokenizer, device)
# 初始化資料庫
db_manager = DatabaseManager(DB_PATH, embedding_model)
db_manager.search_data("Which work environments prohibit smoking?", 5,show=True)