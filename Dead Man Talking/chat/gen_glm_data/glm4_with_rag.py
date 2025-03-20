"""
This script creates an interactive web demo for the GLM-4-9B model using Gradio,
a Python library for building quick and easy UI components for machine learning models.
It's designed to showcase the capabilities of the GLM-4-9B model in a user-friendly interface,
allowing users to interact with the model through a chat-like interface.

Note:
    Using with glm-4-9b-chat-hf will require `transformers>=4.46.0".
"""

import os
from pathlib import Path
from threading import Thread
from typing import Annotated, Union
from rag_database import DatabaseManager
from langchain_ollama import OllamaEmbeddings
import typer
import gradio as gr
import torch
from peft import AutoPeftModelForCausalLM, PeftModelForCausalLM
from transformers import (
    AutoModel,
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    StoppingCriteria,
    StoppingCriteriaList,
    TextIteratorStreamer
)
# base
# ModelType = Union[PreTrainedModel, PeftModelForCausalLM]
# TokenizerType = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]

# MODEL_PATH = os.environ.get('MODEL_PATH', 'THUDM/glm-4-9b-chat')
# TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)


# def _resolve_path(path: Union[str, Path]) -> Path:
#     return Path(path).expanduser().resolve()

# base
# def load_model_and_tokenizer(
#         model_dir: Union[str, Path], trust_remote_code: bool = True
# ) -> tuple[ModelType, TokenizerType]:
#     model_dir = _resolve_path(model_dir)
#     if (model_dir / 'adapter_config.json').exists():
#         model = AutoPeftModelForCausalLM.from_pretrained(
#             model_dir, trust_remote_code=trust_remote_code, device_map='auto'
#         )
#         tokenizer_dir = model.peft_config['default'].base_model_name_or_path
#     else:
#         model = AutoModelForCausalLM.from_pretrained(
#             model_dir, trust_remote_code=trust_remote_code, device_map='auto'
#         )
#         tokenizer_dir = model_dir
#     tokenizer = AutoTokenizer.from_pretrained(
#         tokenizer_dir, trust_remote_code=trust_remote_code, use_fast=False
#     )
#     return model, tokenizer

def load_model_and_tokenizer(
    model_dir: Union[str, Path], trust_remote_code: bool = True
):
    model_dir = Path(model_dir).expanduser().resolve()
    if (model_dir / "adapter_config.json").exists():
        import json

        with open(model_dir / "adapter_config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
        model = AutoModel.from_pretrained(
            config.get("base_model_name_or_path"),
            trust_remote_code=trust_remote_code,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
        model = PeftModelForCausalLM.from_pretrained(
            model=model,
            model_id=model_dir,
            trust_remote_code=trust_remote_code,
        )
        tokenizer_dir = model.peft_config["default"].base_model_name_or_path
    else:
        model = AutoModel.from_pretrained(
            model_dir,
            trust_remote_code=trust_remote_code,
            device_map="auto",
            torch_dtype=torch.bfloat16,
        )
        tokenizer_dir = model_dir
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_dir,
        trust_remote_code=trust_remote_code,
        encode_special_tokens=True,
        use_fast=False,
    )
    return model, tokenizer
model_dir="finetune_demo/output/lora/checkpoint-3000/"
model, tokenizer = load_model_and_tokenizer(model_dir)
embeddings = OllamaEmbeddings(model="llama3")
DB_PATH = "Jim"
db_manager = DatabaseManager(DB_PATH, embeddings)

class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        stop_ids = model.config.eos_token_id
        for stop_id in stop_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False


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
    context=db_manager.search_data(messages[-1]['content'],5)
    print("\n")
    role="Jim程建評"
    rag_message=f"你是{role}，在回答問題之前，我會從你的訓練資料裡面提取出一些可能相關的對話做為參考，你的回應是{role}講的話，你只要參考該對話與問題後，正常回答即可。\n以下為問題:\n{messages[-1]['content']}\n以下為可能相關的對話:\n{context}"
    print(rag_message)
    model_inputs = tokenizer.apply_chat_template(rag_message,
                                                 add_generation_prompt=True,
                                                 tokenize=True,
                                                 return_tensors="pt").to(next(model.parameters()).device)
    streamer = TextIteratorStreamer(tokenizer, timeout=6000, skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = {
        "input_ids": model_inputs,
        "streamer": streamer,
        "max_new_tokens": max_length,
        "do_sample": True,
        "top_p": top_p,
        "temperature": temperature,
        "stopping_criteria": StoppingCriteriaList([stop]),
        "repetition_penalty": 1.2,
        "eos_token_id": model.config.eos_token_id,
    }
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()
    for new_token in streamer:
        if new_token:
            history[-1][1] += new_token
        yield history
    # history[-1][1] += "\n本次rag用到的context:\n"

    # yield history
    

with gr.Blocks() as demo:
    gr.HTML("""<h1 align="center">GLM-4-9B Gradio Simple Chat Demo</h1>""")
    chatbot = gr.Chatbot()

    with gr.Row():
        with gr.Column(scale=3):
            with gr.Column(scale=12):
                user_input = gr.Textbox(show_label=False, placeholder="Input...", lines=10, container=False)
            with gr.Column(min_width=32, scale=1):
                submitBtn = gr.Button("Submit")
        with gr.Column(scale=1):
            prompt_input = gr.Textbox(show_label=False, placeholder="Prompt", lines=10, container=False)
            pBtn = gr.Button("Set Prompt")
        with gr.Column(scale=1):
            emptyBtn = gr.Button("Clear History")
            max_length = gr.Slider(0, 32768, value=8192, step=1.0, label="Maximum length", interactive=True)
            top_p = gr.Slider(0, 1, value=0.8, step=0.01, label="Top P", interactive=True)
            temperature = gr.Slider(0.01, 10, value=0.6, step=0.01, label="Temperature", interactive=True)


    def user(query, history):
        return "", history + [[query, ""]]


    def set_prompt(prompt_text):
        return [[prompt_text, "成功设置prompt"]]


    pBtn.click(set_prompt, inputs=[prompt_input], outputs=chatbot)

    submitBtn.click(user, [user_input, chatbot], [user_input, chatbot], queue=False).then(
        predict, [chatbot, prompt_input, max_length, top_p, temperature], chatbot
    )
    emptyBtn.click(lambda: (None, None), None, [chatbot, prompt_input], queue=False)

demo.queue()
demo.launch(server_name="127.0.0.1", server_port=8000, inbrowser=True, share=True)
