import os

class WriteData:
    def __init__(self, run_dir="run", prefix=""):
        self.run_dir = run_dir
        self.prefix = prefix

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
