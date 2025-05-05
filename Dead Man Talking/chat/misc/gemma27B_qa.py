from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from rag_database import DatabaseManager, CustomEmbedding
from transformers import AutoTokenizer as E5Tokenizer, AutoModel as E5Model

# 初始化生成式模型
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-27b-it")
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-27b-it",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 初始化 Embedding 模型
tok = E5Tokenizer.from_pretrained('intfloat/multilingual-e5-base')
mod = E5Model.from_pretrained('intfloat/multilingual-e5-base').half().to(device)
embedding_model = CustomEmbedding(mod, tok, device)

# 初始化資料庫
DB_PATH = "Law"
db_manager = DatabaseManager(DB_PATH, embedding_model)

# 讀取所有關鍵字
with open("keyword.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f if line.strip()]

# 儲存所有 QA 結果
all_qa_results = []

# 遍歷所有關鍵字並生成 QA
for i, keyword in enumerate(keywords, 1):
    print(f"🔍 [{i}/{len(keywords)}] 處理關鍵字: {keyword}")
    
    try:
        context = db_manager.search_data(keyword, 5)
        # input_text = (
        #     f"請參考以下法律條文來產生5個特定主題的常見問答QA，"
        #     f"每個QA須包含一個問句及一個答句，格式如下"
        #     f"問句:(請填入問句1)\n答句:(請填入答句1)\n問句:(請填入問句2)\n答句:(請填入答句2)\n問句:(請填入問句3)\n答句:(請填入答句3)\n問句:(請填入問句4)\n答句:(請填入答句4)\n問句:(請填入問句5)\n答句:(請填入答句5)\n"
        #     f"特定主題:{keyword}，法條片段:{context}"
        # )
        input_text = (
            f"請參考以下法律條文來產生5個特定主題的常見問答QA，"
            f"每個QA須包含一個問句及一個答句，格式如下"
            f"關鍵字:(請填入關鍵字1)\n問句:(請填入問句1)\n答句:(請填入答句1)\n關鍵字:(請填入關鍵字2)\n問句:(請填入問句2)\n答句:(請填入答句2)\n關鍵字:(請填入關鍵字3)\n問句:(請填入問句3)\n答句:(請填入答句3)\n關鍵字:(請填入關鍵字4)\n問句:(請填入問句4)\n答句:(請填入答句4)\n關鍵字:(請填入關鍵字5)\n問句:(請填入問句5)\n答句:(請填入答句5)\n"
            f"特定主題:{keyword}，法條片段:{context}"
        )

        input_ids = tokenizer(input_text, return_tensors="pt").to(device)
        outputs = model.generate(**input_ids, max_new_tokens=1024)
        generated_ids = outputs[0][input_ids['input_ids'].shape[1]:]
        output_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

        # 將結果儲存進變數
        qa_block = f"🔑 關鍵字: {keyword}\n{output_text}\n{'='*60}\n"
        all_qa_results.append(qa_block)

        print(qa_block)

    except Exception as e:
        error_msg = f"❌ 發生錯誤於關鍵字「{keyword}」: {e}\n{'='*60}\n"
        all_qa_results.append(error_msg)
        print(error_msg)

# 將所有 QA 寫入檔案
with open("qa2.txt", "w", encoding="utf-8") as f:
    f.writelines(all_qa_results)

print("✅ 所有 QA 結果已寫入 qa.txt")
