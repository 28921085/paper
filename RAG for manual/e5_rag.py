import torch
from transformers import AutoTokenizer, AutoModel
from rag_database import DatabaseManager, CustomEmbedding
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


# GPU 裝置檢查
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')



# # 初始化模型
# tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-base-v2')
# model = AutoModel.from_pretrained('intfloat/e5-base-v2').half().to(device)

# 初始化模型
tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-base').half().to(device)

# 初始化 Embedding 類別
embedding_model = CustomEmbedding(model, tokenizer, device)

def parse_conversation(file_path):
    conversations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        conversation_parts = text_splitter.split_text(content)

        for part in conversation_parts:
            conversations.append(Document(page_content=part.strip()))

    return conversations
DB_PATH = "Manual"
file_paths = ["manual.txt"]
# DB_PATH = "Law"
# file_paths = ["law.txt"]
# DB_PATH = "Jim"
# file_paths = [f"conversation/jim-{i}.txt" for i in range(1, 8)]

parsed_conversations = []
for file in file_paths:
    conversations = parse_conversation(file)
    parsed_conversations.extend(conversations)

# 初始化資料庫
db_manager = DatabaseManager(DB_PATH, embedding_model, parsed_conversations)
db_manager.search_data("Which work environments prohibit smoking?", 10,show=True)
