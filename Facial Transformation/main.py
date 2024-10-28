from load_data import LoadData
from write_data import WriteData
from process_image import ProcessImage
from diffusers import StableDiffusionInpaintPipeline
from diffusers import AutoPipelineForInpainting
import torch
from PIL import Image, ImageOps
import os
def run_diffusion_inpaint_test():
    # 初始化 Stable Diffusion Inpainting 模型
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-inpainting",
        torch_dtype=torch.float16,
    ).to("cuda")

    # 初始化 LoadData 和 WriteData
    data_loader = LoadData(dataset_dir="test",max_image=99999)
    writer = WriteData(prefix="p")

    # 創建 run 資料夾
    save_folder = writer.create_run_folder()

    # 載入圖片資料
    image_path_list = data_loader.load_data()

    # 處理並儲存每張圖像
    for image_path in image_path_list:
        print(f"Processing {image_path}")
        
        # 載入圖片
        image = Image.open(image_path).convert("RGB")

        # 自動創建遮罩
        mask = ImageOps.invert(image.convert("L"))  # 將圖片轉換為灰度並取反
        mask = mask.point(lambda x: 255 if x < 1 else 0)  # 將白色像素設為遮罩區域
        mask = mask.convert("1")  # 將遮罩轉為二值圖像
        
        
        # 可選：檢查遮罩
        #mask.show()

        # 使用 Stable Diffusion Inpainting 進行填補
        prompt = "Fill the blank areas with skin texture that matches the surrounding skin tone and texture, creating a seamless blend with the nearby skin without adding any facial features."
        output = pipe(prompt=prompt, image=image, mask_image=mask).images[0]

        # 保存結果，文件名使用原始名稱加上 _output 後綴
        file_name = os.path.basename(image_path)
        output_filename = f"{save_folder}/{file_name}"
        output.save(output_filename)
        print(f"Saved output to {output_filename}")
def run_kandinsky_inpaint_test():
    # 初始化 Kandinsky 2.2 Inpainting 模型
    pipe = AutoPipelineForInpainting.from_pretrained(
        "kandinsky-community/kandinsky-2-2-decoder-inpaint", torch_dtype=torch.float16
    ).to("cuda")

    # 初始化 LoadData 和 WriteData
    data_loader = LoadData(dataset_dir="test", max_image=99999)
    writer = WriteData(prefix="K")

    # 創建 run 資料夾
    save_folder = writer.create_run_folder()

    # 載入圖片資料
    image_path_list = data_loader.load_data()

    # 處理並儲存每張圖像
    for image_path in image_path_list:
        print(f"Processing {image_path}")
        
        # 載入圖片
        image = Image.open(image_path).convert("RGB")

        # 自動創建遮罩
        mask = ImageOps.invert(image.convert("L"))  # 將圖片轉換為灰度並取反
        mask = mask.point(lambda x: 255 if x < 1 else 0)  # 將白色像素設為遮罩區域
        mask = mask.convert("1")  # 將遮罩轉為二值圖像
        
        # 模糊處理遮罩
        #mask = pipe.mask_processor.blur(mask, blur_factor=20)

        # 使用 Kandinsky 進行 Inpainting 填補
        prompt = "Fill the blank areas with skin texture that matches the surrounding skin tone and texture, creating a seamless blend with the nearby skin without adding any facial features."
        output = pipe(prompt=prompt, image=image, mask_image=mask).images[0]

        # 保存結果，文件名使用原始名稱加上 _output 後綴
        file_name = os.path.basename(image_path)
        output_filename = f"{save_folder}/{file_name}"
        output.save(output_filename)
        print(f"Saved output to {output_filename}")

def generate_processed_image():
    # 初始化 LoadData 和 WriteData 類別
    data_loader = LoadData(dataset_dir="dataset/FFHQ dataset/thumbnails128x128")
    writer = WriteData()
    image_processor = ProcessImage()

    # 創建 run 資料夾
    save_folder = writer.create_run_folder()

    # 載入圖像資料
    image_path_list = data_loader.load_data()

    # 處理並儲存每張圖像
    for image_path in image_path_list:
        image_processor.process_image(image_path, save_folder)

#generate_processed_image()
#run_diffusion_inpaint_test()
run_kandinsky_inpaint_test()
