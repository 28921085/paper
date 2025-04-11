import os
from pathlib import Path
from threading import Thread
from typing import Union
import gradio as gr
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    StoppingCriteria,
    StoppingCriteriaList,
    AutoModel,
)
from rag_database import DatabaseManager, CustomEmbedding

# 使用 Gemma 模型
tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b-it")
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-7b-it",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 使用 multilingual-e5-base 作為 RAG 的 embedding 模型
embed_tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-base")
embed_model = AutoModel.from_pretrained("intfloat/multilingual-e5-base").half().to(device)
embedding_model = CustomEmbedding(embed_model, embed_tokenizer, device)

# 設定資料庫位置
DB_PATH = "Law"
db_manager = DatabaseManager(DB_PATH, embedding_model)
role = "assistant"

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        return input_ids[0][-1] in [tokenizer.eos_token_id]

def predict(history, prompt, max_length, top_p, temperature):
    stop = StopOnTokens()
    messages = []
    if prompt:
        messages.append({"role": "system", "content": prompt})
    for idx, (user_msg, model_msg) in enumerate(history):
        if prompt and idx == 0:
            continue
        if idx == len(history) - 1 and not model_msg:
            messages.append({"role": "user", "content": user_msg})
            break
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})
    
    question = messages[-1]['content']
    context = db_manager.search_data(question, 5)
    print(question)
    print(context)
    rag_prompt = (
        f"請參考以下法律條文來產生5個特定主題的常見問答QA，每個QA須包含一個問句及一個答句，特定主題:{question}，法條片段:{context}"
    )

    model_inputs = tokenizer(rag_prompt, return_tensors="pt").to(model.device)
    streamer = TextIteratorStreamer(tokenizer, timeout=6000, skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = {
        "input_ids": model_inputs["input_ids"],
        "streamer": streamer,
        "max_new_tokens": max_length,
        "do_sample": True,
        "top_p": top_p,
        "temperature": temperature,
        "stopping_criteria": StoppingCriteriaList([stop]),
        "repetition_penalty": 1.2,
        "eos_token_id": tokenizer.eos_token_id,
    }
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()
    for new_token in streamer:
        if new_token:
            history[-1][1] += new_token
        yield history

with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">Gemma + RAG 法律問答 Demo</h1>""")
    chatbot = gr.Chatbot()

    with gr.Row():
        with gr.Column(scale=3):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="請輸入問題...", lines=10, container=False)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("送出")
        with gr.Column(scale=1):
            prompt_input = gr.Textbox(show_label=False, placeholder="提示 Prompt", lines=10, container=False)
            pBtn = gr.Button("設定 Prompt")
        with gr.Column(scale=1):
            emptyBtn = gr.Button("清除紀錄")
            max_length = gr.Slider(0, 2048, value=1024, step=1.0, label="回應長度", interactive=True)
            top_p = gr.Slider(0, 1, value=0.8, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0.01, 10, value=0.6, step=0.01, label="Temperature", interactive=True)

    def user(query, history):
        return "", history + [[query, ""]]

    def set_prompt(prompt_text):
        return [[prompt_text, "成功設定 Prompt"]]

    pBtn.click(set_prompt, inputs=[prompt_input], outputs=chatbot)

    submitBtn.click(user, [user_input, chatbot], [user_input, chatbot], queue=False).then(
        predict, [chatbot, prompt_input, max_length, top_p, temperature], chatbot
    )
    emptyBtn.click(lambda: (None, None), None, [chatbot, prompt_input], queue=False)

demo.queue()
demo.launch(server_name="127.0.0.1", server_port=8000, inbrowser=True, share=True)
