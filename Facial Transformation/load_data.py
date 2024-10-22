import os
import random
import cv2
import dlib
import numpy as np

def list_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        file_names = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
        return file_names
    except FileNotFoundError:
        return "指定的路徑不存在，請檢查路徑是否正確。"
    except Exception as e:
        return f"發生錯誤: {str(e)}"

def load_data(max_image=5):
    directory_path = os.path.join(".", "dataset", "FFHQ dataset", "thumbnails128x128")
    file_list = list_files_in_directory(directory_path)
    random.shuffle(file_list)

    image_path_list = []
    if isinstance(file_list, list):
        cnt = 0
        for file_name in file_list:
            image_path = os.path.join(".", "dataset", "FFHQ dataset", "thumbnails128x128", file_name)
            image_path_list.append(image_path)
            cnt += 1
            if cnt == max_image:
                break
    else:
        print(file_list)  # 錯誤訊息
    return image_path_list

def create_run_folder():
    run_folder = os.path.join(".", "run")
    if not os.path.exists(run_folder):
        os.makedirs(run_folder)

    existing_ids = [int(folder) for folder in os.listdir(run_folder) if folder.isdigit()]
    next_id = max(existing_ids) + 1 if existing_ids else 0

    new_folder_path = os.path.join(run_folder, str(next_id))
    os.makedirs(new_folder_path)
    
    return new_folder_path

def process_image(image_path, save_folder):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(os.path.join(".", "model", "shape_predictor_68_face_landmarks.dat"))
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # 獲取眼睛、鼻子、嘴巴的特徵點範圍
        left_eye_points = list(range(36, 42))  # 左眼
        right_eye_points = list(range(42, 48))  # 右眼
        nose_points = list(range(27, 36))  # 鼻子
        mouth_points = list(range(48, 68))  # 嘴巴

        # 函數來挖空每個區域
        def fill_white(points):
            pts = np.array([[landmarks.part(p).x, landmarks.part(p).y] for p in points], np.int32)
            hull = cv2.convexHull(pts)  # 生成凸包
            cv2.fillPoly(image, [hull], (255, 255, 255))  # 挖空該區域，填充為白色

        # 分別處理左眼、右眼、鼻子和嘴巴
        fill_white(left_eye_points)   # 挖空左眼
        fill_white(right_eye_points)  # 挖空右眼
        fill_white(nose_points)       # 挖空鼻子
        fill_white(mouth_points)      # 挖空嘴巴

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
