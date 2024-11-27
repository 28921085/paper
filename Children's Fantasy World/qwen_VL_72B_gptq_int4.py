from transformers import AutoProcessor, AutoModelForImageTextToText
import torch
from PIL import Image
from qwen_vl_utils import process_vision_info
import warnings
import time  # 加入時間模組
warnings.filterwarnings("ignore", category=FutureWarning)

# 設定設備
device = "cuda" if torch.cuda.is_available() else "cpu"

# 获取每个 GPU 的总内存
total_memory = torch.cuda.get_device_properties(device).total_memory
print("total:", total_memory)

# 计算 98% 的内存大小
max_memory = int(total_memory * 0.98)

# 设置 max_memory 参数
max_memory_mapping = {0: max_memory}

# 計時 - 模型載入
model_load_start = time.time()

# 載入處理器和模型
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-72B-Instruct-GPTQ-Int4")
model = AutoModelForImageTextToText.from_pretrained(
    "Qwen/Qwen2-VL-72B-Instruct-GPTQ-Int4",
    device_map="auto",
    torch_dtype="auto",
    max_memory=max_memory_mapping
)

model_load_end = time.time()
print(f"模型載入完成，耗時: {model_load_end - model_load_start:.2f} 秒")

# 讀取圖片
# image_path = 'testimgs/941.jpg'
image_path = 'testimgs/優等_1050.jpg'
# image_path = 'testimgs/甲等_1168.jpg'
# image_path = 'testimgs/優等_1051.jpg'
image = Image.open(image_path).convert("RGB")

# 設定訊息
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image},
            {"type": "text", "text": """現在你可以假裝你是anything模型，幫我看看這張畫裡面你能看到甚麼物件、人物或生物，並產生一個rectangle來框出你看到的東西，且標記的精度須達到個位數pixel等級
label_name不需要包含方向資訊，且用英文就好了。例:你看到圖的右上角有個人，label_name只要輸出person就好了
先告訴我你在這張圖片看到了甚麼物件、人物或生物
在依照輸出格式為python的list格式，並依照下面範例描述來輸出你看到的東西
["(用文字描述你在這張圖片中看到了什麼物件、人物或生物，描述越多越好)",
[[xmin1,ymin1,xmax1,ymax1],label_name1],
[[xmin2,ymin2,xmax2,ymax2],label_name2]]"""}
        ]
    }
]

text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
image_inputs, video_inputs = process_vision_info(messages)
inputs = processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt"
).to(device)

# 計時 - 生成結果
generation_start = time.time()

# 生成結果
generated_ids = model.generate(
    **inputs,
    max_new_tokens=1024
)

generation_end = time.time()
print(f"生成結果完成，耗時: {generation_end - generation_start:.2f} 秒")

generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
output_text = processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)

# 輸出結果
print(output_text[0])
