from langchain_ollama import OllamaEmbeddings
from rag_database import DatabaseManager
from langchain.schema import Document

userTag="User"
AITag = "Jim程建評"
def parse_conversation(file_path):
    conversations = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_user = None
    current_assistant = None

    for line in lines:
        if line.startswith("user: "):
            current_user = line.strip().replace("user: ", "")
        elif line.startswith("assistant: ") and current_user:
            current_assistant = line.strip().replace("assistant: ", "")
            conversations.append(f"{userTag}: {current_user} | {AITag}: {current_assistant}")
            current_user = None

    return conversations
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
DB_PATH = "Jim"

# 讀取並解析檔案
# file_paths = [f"conversation/jim-{i}_output.txt" for i in range(1, 8)]
file_paths = [f"conversation/jim-{i}.txt" for i in range(1, 8)]
parsed_conversations = []
for file in file_paths:
    conversation = parse_conversation(file)
    for data in conversation:
        parsed_conversations.append(Document(page_content=data))  # ✅ 修正點：轉換為 Document

# 初始化資料庫
db_manager = DatabaseManager(DB_PATH, embeddings, parsed_conversations)

# 測試查詢
db_manager.search_data("Jim對擇偶有什麼條件",20)