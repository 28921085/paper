from langchain_ollama import OllamaEmbeddings
from rag_database import DatabaseManager
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

userTag="User"
AITag = "Jim程建評"
def parse_conversation(file_path):
    conversations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # 讀取整個檔案
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
        conversation_parts = text_splitter.split_text(content)  # 🔹 適用於純文字

        # 將每一段轉為 Document 物件
        for part in conversation_parts:
            conversations.append(Document(page_content=part.strip()))

    return conversations
# def parse_conversation(file_path):
#     conversations = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     current_user = None
#     current_assistant = None

#     for line in lines:
#         if line.startswith("user: "):
#             current_user = line.strip().replace("user: ", "")
#         elif line.startswith("assistant: ") and current_user:
#             current_assistant = line.strip().replace("assistant: ", "")
#             conversations.append(f"{userTag}: {current_user} | {AITag}: {current_assistant}")
#             current_user = None

#     return conversations
# # 🔹 讀取並解析檔案
# def parse_conversation(file_path):
#     conversations = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     current_conversation = []

#     for line in lines:
#         if line.strip() == "":  # 空白行標示一段對話的結束
#             if current_conversation:
#                 conversations.append("\n".join(current_conversation))
#                 current_conversation = []
#         elif line.startswith("user: "):
#             current_conversation.append(f"{userTag}: {line.strip().replace('user: ', '')}")
#         elif line.startswith("assistant: "):
#             current_conversation.append(f"{AITag}: {line.strip().replace('assistant: ', '')}")
#         else:
#             current_conversation.append(line.strip())

#     if current_conversation:  # 檔案末尾的對話
#         conversations.append("\n".join(current_conversation))

#     return conversations

embeddings = OllamaEmbeddings(model="llama3")
# DB_PATH = "Jim"
DB_PATH = "Law"

# 讀取並解析檔案
# file_paths = [f"conversation/jim-{i}_output.txt" for i in range(1, 8)]
# file_paths = [f"conversation/jim-{i}.txt" for i in range(1, 8)]
file_paths = ["law.txt"]
parsed_conversations = []
# for file in file_paths:
#     conversation = parse_conversation(file)
#     for data in conversation:
#         parsed_conversations.append(Document(page_content=data))  # ✅ 修正點：轉換為 Document


for file in file_paths:
    conversations = parse_conversation(file)
    parsed_conversations.extend(conversations)  # ✅ 將分割後的對話加入陣列

# 初始化資料庫
db_manager = DatabaseManager(DB_PATH, embeddings, parsed_conversations)

# 測試查詢
db_manager.search_data("未成年人", 20)