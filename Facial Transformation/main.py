from load_data import LoadData
from write_data import WriteData
from process_image import ProcessImage
from diffusion_models import *

def generate_processed_image():
    # 初始化 LoadData 和 WriteData 類別
    data_loader = LoadData(dataset_dir="dataset/FFHQ dataset/thumbnails128x128")
    #data_loader = LoadData(dataset_dir="dataset/Other")
    writer = WriteData()
    image_processor = ProcessImage()

    # 載入圖像資料
    image_path_list = data_loader.load_data()

    # 處理並儲存每張圖像
    for image_path in image_path_list:
        image = image_processor.process_image(image_path)
        writer.save_png_cv2(image,image_path)

generate_processed_image()

# # diffusion_models.py (目前擱置中)   env 'inpainting'
# run_diffusion_inpaint_test()
# run_kandinsky_inpaint_test()
# TODO prompt也存下來   