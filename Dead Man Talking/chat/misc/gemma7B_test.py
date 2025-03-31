# pip install accelerate
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from rag_database import DatabaseManager, CustomEmbedding
from transformers import AutoTokenizer, AutoModel
# tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b-it")
# model = AutoModelForCausalLM.from_pretrained(
#     "google/gemma-7b-it",
#     device_map="auto",
#     torch_dtype=torch.bfloat16,
# )
tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b-it")
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-7b-it",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tok = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base')
mod = AutoModel.from_pretrained('intfloat/multilingual-e5-base').half().to(device)

# 初始化 Embedding 類別
embedding_model = CustomEmbedding(mod, tok, device)
DB_PATH = "Jim"
# DB_PATH = "Law"
db_manager = DatabaseManager(DB_PATH, embedding_model)
role="assistant"
question="你的理想型是?"
# question="未成年人有甚麼權利及義務?"
context=db_manager.search_data(question,5)
input_text = f"你是{role}，請參考上下文的資訊及回答風格來回答問題。以下為問題:{question}，以下為上下文:\n{context}"
# input_text=f"請參考以下法律條文的片段來回答此法律問題，問題:{question}，法條片段:{context}"
input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")
print("-------gemma-------")
outputs = model.generate(**input_ids, max_new_tokens=1024)
print(tokenizer.decode(outputs[0]))
