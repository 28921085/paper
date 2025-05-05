# interactive_test.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 只載入一次 fine-tuned 模型
model_dir = "lora_gemma_adapter"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", torch_dtype=torch.bfloat16)
model.eval()

def ask_question(question: str) -> str:
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
    answer = response.split("<start_of_turn>model\n")[-1].strip()
    return answer

# 啟動互動式迴圈
print("🔁 啟動問答模式，輸入 'exit' 可離開")

while True:
    question = input("💬 請輸入你的問題：")
    if question.lower() in ["exit", "quit"]:
        print("👋 結束問答")
        break

    answer = ask_question(question)

    print(f"🤖 回答：{answer}")

    # 儲存對話記錄
    with open("qa_record.txt", "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\nA: {answer}\n\n")
