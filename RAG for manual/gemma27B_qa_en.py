from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from rag_database import DatabaseManager, CustomEmbedding
from transformers import AutoTokenizer as E5Tokenizer, AutoModel as E5Model
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# 1️⃣ 初始化生成模型（Gemma）
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-27b-it")
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-27b-it",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 2️⃣ 初始化 Embedding 模型（E5）
tok = E5Tokenizer.from_pretrained('intfloat/multilingual-e5-base')
mod = E5Model.from_pretrained('intfloat/multilingual-e5-base').half().to(device)
embedding_model = CustomEmbedding(mod, tok, device)


# 4️⃣ 載入 manual.txt 並切割成 chunks
with open("manual.txt", "r", encoding="utf-8") as f:
    content = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_text(content)

# 5️⃣ 建立 QA 結果容器
all_qa_results = []

# 6️⃣ 遍歷每個 chunk，產生 QA
for i, chunk in enumerate(chunks, 1):
    print(f"🔍 [{i}/{len(chunks)}] 處理區塊...")

    try:
        input_text = (
            f"You are currently reading the company's employee handbook. Please refer to the following text and generate 3 common Q&A pairs. "
            f"Each pair should include a **keyword**, a **question**, and an **answer**, formatted as follows:\n"
            f"Keyword: (Insert keyword 1)\nQuestion: (Insert question 1)\nAnswer: (Insert answer 1)\n"
            f"Keyword: (Insert keyword 2)\nQuestion: (Insert question 2)\nAnswer: (Insert answer 2)\n"
            f"Keyword: (Insert keyword 3)\nQuestion: (Insert question 3)\nAnswer: (Insert answer 3)\n\n"
            f"Below is the text content:\n{chunk}"
        )

        input_ids = tokenizer(input_text, return_tensors="pt").to(device)
        outputs = model.generate(**input_ids, max_new_tokens=1024)
        generated_ids = outputs[0][input_ids['input_ids'].shape[1]:]
        output_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

        qa_block = f"🧩 Chunk {i}:\n{output_text}\n{'='*60}\n"
        all_qa_results.append(qa_block)
        print(qa_block)

    except Exception as e:
        error_msg = f"❌ 發生錯誤於 chunk {i}: {e}\n{'='*60}\n"
        all_qa_results.append(error_msg)
        print(error_msg)

# 7️⃣ 輸出所有 QA 到檔案
with open("qa_from_chunks.txt", "w", encoding="utf-8") as f:
    f.writelines(all_qa_results)

print("✅ 所有 QA 結果已寫入 qa_from_chunks.txt")
