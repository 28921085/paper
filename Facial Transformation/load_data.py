import os
import random
import cv2
import dlib
from PIL import Image

def list_files_in_directory(directory_path):
    try:
        # 使用 os.listdir() 列出資料夾內的所有檔案與目錄
        files = os.listdir(directory_path)
        
        # 過濾出檔案（排除子目錄）
        file_names = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
        
        # 回傳檔案名稱清單
        return file_names
    
    except FileNotFoundError:
        return "指定的路徑不存在，請檢查路徑是否正確。"
    except Exception as e:
        return f"發生錯誤: {str(e)}"
def load_data(max_image=5):
    # 使用範例，這裡使用相對路徑 (要開啟資料夾facial transformation)
    directory_path = os.path.join(".","dataset", "FFHQ dataset","thumbnails128x128")  # 替換為相對路徑
    #print(directory_path)
    file_list = list_files_in_directory(directory_path)
    random.shuffle(file_list) 

    image_path_list=[]

    if isinstance(file_list, list):
        cnt=0
        for file_name in file_list:
            image_path = os.path.join(".","dataset", "FFHQ dataset","thumbnails128x128",file_name)
            image_path_list.append(image_path)

            cnt+=1
            if cnt==max_image:
                break
    else:
        print(file_list)  # 錯誤訊息
    return image_path_list

def create_run_folder():
    # 找到run資料夾內的最大id
    run_folder = os.path.join(".", "run")
    if not os.path.exists(run_folder):
        os.makedirs(run_folder)  # 如果run資料夾不存在，建立它

    existing_ids = [int(folder) for folder in os.listdir(run_folder) if folder.isdigit()]
    next_id = max(existing_ids) + 1 if existing_ids else 0  # 如果資料夾不存在，則從0開始

    new_folder_path = os.path.join(run_folder, str(next_id))
    os.makedirs(new_folder_path)
    
    return new_folder_path

def process_image(image_path, save_folder):
    # 載入dlib的面部檢測器
    detector = dlib.get_frontal_face_detector()

    # 載入dlib的預訓練模型，該模型檢測68個面部特徵點
    predictor = dlib.shape_predictor(os.path.join(".", "model", "shape_predictor_68_face_landmarks.dat"))
    image = cv2.imread(image_path)
    
    # 將圖片轉換為灰度圖像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 檢測面部
    faces = detector(gray)
    
    for face in faces:
        # 預測五官位置
        landmarks = predictor(gray, face)
        
        # 將每個特徵點繪製到圖片上
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(image, (x, y), 2, (255, 0, 0), -1)  # 使用藍色圓點標記五官位置
        
    # 構建存儲路徑
    file_name = os.path.basename(image_path)
    save_path = os.path.join(save_folder, file_name)
    
    # 儲存圖片
    cv2.imwrite(save_path, image)
    print(f"已儲存圖片至: {save_path}")


# 創建新的run資料夾
save_folder = create_run_folder()

# 載入圖像資料
image_path_list = load_data()

# 處理並儲存每張圖像
for image_path in image_path_list:
    process_image(image_path, save_folder)