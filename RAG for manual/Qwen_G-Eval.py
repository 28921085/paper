from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from rag_database import DatabaseManager, CustomEmbedding
from transformers import AutoTokenizer as E5Tokenizer, AutoModel as E5Model
import torch
# 模型名稱：Qwen-14B Chat 版本（更適合對話與推論）
# model_id = "Qwen/Qwen-14B-Chat"
# model_id = "Qwen/Qwen3-32B"
model_id = "Qwen/Qwen2.5-32B-Instruct"

# 載入 tokenizer 和模型（第一次會下載，需較大記憶體）
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",  # 自動選擇 GPU/CPU
    trust_remote_code=True,
    torch_dtype="auto"
)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 初始化 Embedding 模型
tok = E5Tokenizer.from_pretrained('intfloat/multilingual-e5-base')
mod = E5Model.from_pretrained('intfloat/multilingual-e5-base').half().to(device)
embedding_model = CustomEmbedding(mod, tok, device)

# 初始化資料庫
DB_PATH = "Law"
db_manager = DatabaseManager(DB_PATH, embedding_model)


# 使用 transformers pipeline 快速生成
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

def extract_answers(file_path):
    answers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("A:"):
                answer = line[2:].strip()
                if answer:  # 忽略空的 A:
                    answers.append(answer)
    return answers

# 定義 extract_question 函式
def extract_questions(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Q:"):
                question = line[2:].strip()
                if question:  # 忽略空的 Q:
                    questions.append(question)
    return questions

qa_ex_answers = extract_answers("qa_ex.txt")
qa_record_answers = extract_answers("qa_record.txt")
qa_record_questions = extract_questions("qa_record.txt")

results = []

for idx, (question, model_ans, ref_answer) in enumerate(zip(qa_record_questions, qa_record_answers, qa_ex_answers), 1):
    # 模擬 context 結果（此處簡化，實際應由 db_manager.search_data 提供）
    context = db_manager.search_data(question, 3)

    # 建立 prompt
    prompt = f'''你是一位具備民法專業知識的助教，請根據以下三個面向評估模型的回答品質：

        1. 【正確性】：模型的回答是否符合民法條文與法律原則？這邊請幫我依據上下文的台灣民法法條推斷，滿分為 5 分。
        2. 【完整性】：模型是否有涵蓋必要的法律要件與條件？，滿分為 5 分。
        3. 【表達清晰】：語言是否通順、易懂、沒有模糊或歧義？，滿分為 5 分。

        請依據下方的問題、模型回答與參考答案，逐項分析並解釋你的評分理由（chain-of-thought），再填入以下評分表單：

        問題： {question}
        模型回答： {model_ans}
        參考答案： {ref_answer}
        上下文： {context}

        輸出請照著以下格式輸出：
        一段簡評: (簡評)

        | 評分項目 | 滿分 | 實得分 | 評分原因（請使用法律分析方式進行說明） |
        |----------|------|--------|----------------------------------------|
        | 正確性   | 5    | ?      | …                                       |
        | 完整性   | 5    | ?      | …                                       |
        | 表達清晰 | 5    | ?      | …                                       |
        '''
     # 套用對話格式提示
    system_prompt = f"""<|im_start|>user
        {prompt}<|im_end|>
        <|im_start|>assistant
        """
    # 模型產生回答（不帶入過去上下文）
    output = chatbot(system_prompt, max_new_tokens=512, do_sample=False)[0]["generated_text"]
    response = output.split("<|im_start|>assistant\n")[-1].strip()
    results.append(f"【第 {idx} 題】\n問題：{question}\n模型回答：{model_ans}\n參考答案：{ref_answer}\n\n{response}\n{'='*80}\n")
    print(f"【第 {idx} 題】\n問題：{question}\n模型回答：{model_ans}\n參考答案：{ref_answer}\n\n{response}\n{'='*80}\n")
# 寫入檔案
output_file = "G-EVAL.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(results)
