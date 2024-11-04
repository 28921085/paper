from load_data import LoadData
from write_data import WriteData
from process_image import ProcessImage
from diffusion_models import *
import cv2

# conda env 'inpainting'

def generate_processed_image():
    # 初始化 LoadData 和 WriteData 類別
    #data_loader = LoadData(dataset_dir="dataset/FFHQ dataset/thumbnails128x128")
    data_loader = LoadData(dataset_dir="dataset/Other")
    writer = WriteData()
    image_processor = ProcessImage()

    # 載入圖像資料
    image_path_list = data_loader.load_data()

    # 處理並儲存每張圖像
    for image_path in image_path_list:
        image = image_processor.process_image(image_path)
        #writer.save_png_cv2(image,image_path)
        writer.save_png_cv2(image,image_path)


def opencv_inpaint():
    data_loader = LoadData(dataset_dir="test/test6",max_image=99999)
    writer = WriteData(prefix="o")

    image_path_list = data_loader.load_data()
    for image_path in image_path_list:
        image = cv2.imread(image_path)
        mask = cv2.inRange(image, (254, 254, 254), (255, 255, 255))

        # 使用 inpaint 函數進行圖像修復
        # 使用 cv2.INPAINT_TELEA 方法，另一個選擇是 cv2.INPAINT_NS
        result = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        writer.save_png_cv2(result,image_path)

opencv_inpaint()
#generate_processed_image()

# # diffusion_models.py (目前擱置中)   
# run_diffusion_inpaint_test()
# run_kandinsky_inpaint_test()
# TODO prompt也存下來   