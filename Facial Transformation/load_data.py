import os
import random

class LoadData:
    def __init__(self, dataset_dir="dataset/FFHQ dataset/thumbnails128x128", run_dir="run"):
        self.dataset_dir = dataset_dir
        self.run_dir = run_dir

    def list_files_in_directory(self, directory_path):
        try:
            files = os.listdir(directory_path)
            file_names = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
            return file_names
        except FileNotFoundError:
            return "指定的路徑不存在，請檢查路徑是否正確。"
        except Exception as e:
            return f"發生錯誤: {str(e)}"

    def load_data(self, max_image=5):
        file_list = self.list_files_in_directory(self.dataset_dir)
        if isinstance(file_list, list):
            random.shuffle(file_list)
            return [os.path.join(self.dataset_dir, file_list[i]) for i in range(min(max_image, len(file_list)))]
        else:
            print(file_list)  # 錯誤訊息
            return []

    def create_run_folder(self):
        if not os.path.exists(self.run_dir):
            os.makedirs(self.run_dir)

        existing_ids = [int(folder) for folder in os.listdir(self.run_dir) if folder.isdigit()]
        next_id = max(existing_ids) + 1 if existing_ids else 0
        new_folder_path = os.path.join(self.run_dir, str(next_id))
        os.makedirs(new_folder_path)
        
        return new_folder_path
