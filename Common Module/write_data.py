import os
import cv2
from PIL import Image

class WriteData:
    def __init__(self, run_dir="run", prefix=""):
        self.run_dir = run_dir
        self.prefix = prefix
        self.path = ""

    def create_run_folder(self):
        # 檢查資料夾是否存在，若不存在則建立
        if not os.path.exists(self.run_dir):
            os.makedirs(self.run_dir)

        # 過濾出以指定 prefix 開頭的資料夾名稱，並取得編號部分
        existing_ids = [
            int(folder[len(self.prefix):]) 
            for folder in os.listdir(self.run_dir) 
            if folder.startswith(self.prefix) and folder[len(self.prefix):].isdigit()
        ]

        # 計算下一個編號
        next_id = max(existing_ids) + 1 if existing_ids else 0
        new_folder_path = os.path.join(self.run_dir, f"{self.prefix}{next_id}")
        os.makedirs(new_folder_path)
        
        return new_folder_path
    def write_txt(self,data, filename):
        # 檢查 data 是否為陣列或字串
        if isinstance(data, (list, tuple)):
            # 如果是陣列（list 或 tuple），將每個元素轉成字串並以換行符號分隔
            data_str = "\n".join(map(str, data))
        elif isinstance(data, str):
            # 如果是字串，直接寫入
            data_str = data
        else:
            raise ValueError("儲存txt錯誤，只接受陣列（list、tuple）或字串")

        # 將內容寫入 .txt 檔案
        save_path = os.path.join(self.path, filename)
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(data_str)
        print(f"資料已成功寫入 {save_path}")
    
    def save_img_diffuser(self,output,filename):
        if self.path == "":
            # 創建 run 資料夾
            self.path = self.create_run_folder()

        file_name = os.path.basename(filename)
        output_filename = f"{self.path}\\{file_name}"
        output.save(output_filename)
        print(f"已儲存圖片至: {output_filename}")

    def save_img_cv2(self,image,filename,attached_data=None,attached_data_name="attached_data.txt"):
        if self.path == "":
            # 創建 run 資料夾
            self.path = self.create_run_folder()
        if attached_data:
            self.write_txt(attached_data,attached_data_name)

        file_name = os.path.basename(filename)
        save_path = os.path.join(self.path, file_name)
        cv2.imwrite(save_path, image)
        print(f"已儲存圖片至: {save_path}")
    
    def save_img_PIL(self,image,filename,attached_data=None,attached_data_name="attached_data.txt"):
        if self.path == "":
            # 創建 run 資料夾
            self.path = self.create_run_folder()
        if attached_data:
            self.write_txt(attached_data,attached_data_name)

        file_name = os.path.basename(filename)
        save_path = os.path.join(self.path, file_name)
        image.save(save_path)
        print(f"已儲存圖片至: {save_path}")

