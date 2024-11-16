# Load model directly
from transformers import AutoProcessor, AutoModelForImageTextToText

processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-72B-Instruct")
model = AutoModelForImageTextToText.from_pretrained("Qwen/Qwen2-VL-72B-Instruct")