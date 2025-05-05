from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from trl import SFTTrainer
from peft import LoraConfig
from datasets import load_dataset
import torch

# 1. 模型與 tokenizer 設定
model_id = "google/gemma-2-27b-it"
tokenizer = AutoTokenizer.from_pretrained(model_id)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    quantization_config=bnb_config
)

# 2. LoRA 設定
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "down_proj", "up_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 3. 資料載入與格式化
dataset = load_dataset("json", data_files="qa_ex.jsonl")

def formatting_func(example):
    prompt = example["question"]
    response = example["answer"]
    text = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n{response}<end_of_turn>"
    return text

# 4. 訓練參數（新增 logging_dir 與 report_to）
training_args = TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    warmup_steps=2,
    max_steps=500,
    learning_rate=2e-4,
    fp16=False,
    bf16=True,
    logging_steps=1,
    output_dir="outputs",
    save_strategy="no",
    optim="paged_adamw_8bit",
    logging_dir="./logs",         # ✅ 新增：TensorBoard 記錄目錄
    report_to="tensorboard",      # ✅ 新增：啟用 tensorboard 記錄
)

# 5. 建立 Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    args=training_args,
    peft_config=lora_config,
    formatting_func=formatting_func,
)

# 6. 訓練
trainer.train()

# 7. 儲存微調結果
trainer.model.save_pretrained("lora_gemma_adapter")
tokenizer.save_pretrained("lora_gemma_adapter")

# 8. 使用訓練後模型進行推論
model = trainer.model
model.eval()

def ask_question(question: str):
    prompt = f"<start_of_turn>user\n{question}<end_of_turn>\n<start_of_turn>model\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = response.split("<start_of_turn>model\n")[-1]
    print("💬 問題:", question)
    print("🤖 回答:", answer.strip())

# 9. 測試推論
ask_question("借用物損壞了，借用人需要賠償嗎？詳細說明理由")
