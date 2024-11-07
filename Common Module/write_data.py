import os
import cv2

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
    
    def save_png_diffuser(self,output,filename):
        if self.path == "":
            # 創建 run 資料夾
            self.path = self.create_run_folder()

        file_name = os.path.basename(filename)
        output_filename = f"{self.path}\\{file_name}"
        output.save(output_filename)
        print(f"已儲存圖片至: {output_filename}")

    def save_png_cv2(self,image,filename):
        if self.path == "":
            # 創建 run 資料夾
            self.path = self.create_run_folder()

        file_name = os.path.basename(filename)
        save_path = os.path.join(self.path, file_name)
        cv2.imwrite(save_path, image)
        print(f"已儲存圖片至: {save_path}")

