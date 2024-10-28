from load_data import LoadData
from process_image import ProcessImage

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
