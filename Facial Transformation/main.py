from load_data import LoadData
from process_image import ProcessImage
from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image, ImageOps
import numpy as np
import glob
def run_diffusion_test():
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-inpainting",
        torch_dtype=torch.float16,
    )
    # 循環處理 /test 資料夾中的所有圖片
    for image_path in glob.glob("/test/*.png"):
        print(f"Processing {image_path}")

        # 載入圖片
        image = Image.open(image_path).convert("RGB")

        # 自動創建遮罩
        mask = ImageOps.invert(image.convert("L"))  # 將圖片轉換為灰度並取反
        mask = mask.point(lambda x: 255 if x > 254 else 0)  # 將接近白色的像素設為遮罩區域
        mask = mask.convert("1")  # 將遮罩轉為二值圖像

        # 可選：檢查遮罩
        # mask.show()

        # 使用 Stable Diffusion Inpainting 進行填補
        prompt = "Fill the blank areas naturally"
        output = pipe(prompt=prompt, image=image, mask_image=mask).images[0]

        # 保存結果，文件名使用原始名稱+_output
        output_path = image_path.replace(".png", "_output.png")
        output.save(output_path)
        print(f"Saved output to {output_path}")


def generate_processed_image():
    # 初始化 LoadData 和 ProcessImage 類別
    data_loader = LoadData()
    image_processor = ProcessImage()

    # 創建 run 資料夾
    save_folder = data_loader.create_run_folder()

    # 載入圖像資料
    image_path_list = data_loader.load_data()

    # 處理並儲存每張圖像
    for image_path in image_path_list:
        image_processor.process_image(image_path, save_folder)

generate_processed_image()
#run_diffusion_test()
