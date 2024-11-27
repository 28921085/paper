import torch
from PIL import Image
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from accelerate import init_empty_weights, infer_auto_device_map
# 檢查 CUDA 是否可用，並設定裝置
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 获取每个 GPU 的总内存
total_memory = torch.cuda.get_device_properties(device).total_memory
print("total:",total_memory)
# 计算 98% 的内存大小
max_memory = int(total_memory * 0.98)

# 设置 max_memory 参数
max_memory_mapping = {0: max_memory}
# 載入模型和處理器
model_name = "Qwen/Qwen2-VL-7B-Instruct"
model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # 使用半精度浮點數以節省顯存
    device_map="auto",           # 自動選擇可用設備（GPU 或 CPU）
    max_memory=max_memory_mapping,
    cache_dir="./local_model_cache"
)
processor = AutoProcessor.from_pretrained(model_name)
# 讀取圖片
image_path = "testimgs/941.jpg"  # 替換為您的圖片路徑
# image_path = "testimgs/甲等_1168.jpg"  # 替換為您的圖片路徑
image = Image.open(image_path).convert("RGB")

# 定義對話內容
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
# 處理視覺輸入
image_inputs, video_inputs = process_vision_info(messages)

# 準備輸入
text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = processor(
    text=[text],
    images=image_inputs,
    videos=video_inputs,
    padding=True,
    return_tensors="pt"
)
inputs = inputs.to(model.device)
# 生成結果
generated_ids = model.generate(**inputs, max_new_tokens=1024)
generated_ids_trimmed = [out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)]
output_text = processor.batch_decode(generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)

# 輸出結果
print(output_text[0])
