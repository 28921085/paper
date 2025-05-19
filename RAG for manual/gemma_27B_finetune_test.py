# auto_infer_from_file.py

from transformers import AutoTokenizer, AutoModelForCausalLM,AutoModel
import torch
from rag_database import DatabaseManager, CustomEmbedding

# 載入 fine-tuned 模型
# model_dir = "lora_gemma_adapter" # fine tune
model_dir = "google/gemma-2-27b-it" #base
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", torch_dtype=torch.bfloat16)
model.eval()

#rag
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tok = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-base')
mod = AutoModel.from_pretrained('intfloat/multilingual-e5-base').half().to(device)
embedding_model = CustomEmbedding(mod, tok, device)
# DB_PATH = "Law"
DB_PATH = "Manual"

db_manager = DatabaseManager(DB_PATH, embedding_model)

# 問答函式
def ask_question(question: str) -> str:
    prompt = f"<start_of_turn>user\n{question}<end_of_turn>\n<start_of_turn>model\n" # base

    # context = db_manager.search_data(question, 5,False)
    # print(context)
    # # prompt = f"請閱讀上下文後回答這個問題\n問題:{question}\n上下文{context}\n"
    # prompt = f"Please read the context before answering this question.\nQuestion:{question}\nContext:{context}\n"
    # prompt = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response=response.split("model\n")[-1]
    return response

# 從檔案中擷取問題
def extract_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # return [line.strip()[2:].strip() for line in lines if line.strip().startswith("Q:")]
    return [line.strip()[9:].strip() for line in lines if line.strip().startswith("Question:")]


# 主程式：執行推論與紀錄
questions = extract_questions("qa_ex_en.txt")
# questions = extract_questions("qa_ex.txt")


with open("qa_record.txt", "w", encoding="utf-8") as f:
    for i, question in enumerate(questions, 1):
        answer = ask_question(question)
        print(f"➡️ 正在處理第 {i} 題：{question}")
        print(f"🤖 回答：{answer}\n")
        f.write(f"Q: {question}\nA: {answer}\n\n")

print("✅ 所有問答已完成並儲存至 qa_record.txt")
