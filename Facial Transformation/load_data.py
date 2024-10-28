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

        # 定義眼睛、鼻子和嘴巴的特徵點範圍
        entire_face = list(range(0, 68))  # 整個臉的特徵點
        left_eye_points = list(range(36, 42))  # 左眼
        right_eye_points = list(range(42, 48))  # 右眼
        nose_points = list(range(27, 36))  # 鼻子
        mouth_points = list(range(48, 68))  # 嘴巴

        # 繪製整個臉部邊界
        entire_face_pts = np.array([[landmarks.part(p).x, landmarks.part(p).y] for p in entire_face], np.int32)
        entire_face_hull = cv2.convexHull(entire_face_pts)
        cv2.polylines(image, [entire_face_hull], isClosed=True, color=(255, 0, 0), thickness=2)  

        # 函數來擷取指定多邊形並移動到新位置
        def extract_and_move_polygon(points, new_x, new_y):
            # 獲取特徵點座標，並生成凸包
            pts = np.array([[landmarks.part(p).x, landmarks.part(p).y] for p in points], np.int32)
            hull = cv2.convexHull(pts)

            # 創建遮罩並填充多邊形區域
            mask = np.zeros_like(image)
            cv2.fillPoly(mask, [hull], (255, 255, 255))
            polygon_region = cv2.bitwise_and(image, mask)

            # 擷取多邊形區域
            non_zero_coords = np.where(mask[:, :, 0] == 255)
            min_y, min_x = min(non_zero_coords[0]), min(non_zero_coords[1])
            polygon_cropped = polygon_region[min_y:max(non_zero_coords[0])+1, min_x:max(non_zero_coords[1])+1]
            mask_cropped = mask[min_y:max(non_zero_coords[0])+1, min_x:max(non_zero_coords[1])+1]

            # 使用for迴圈將多邊形範圍內的像素移動到新位置
            for i in range(polygon_cropped.shape[0]):
                for j in range(polygon_cropped.shape[1]):
                    if mask_cropped[i, j, 0] == 255:  # 確保該點在五官形成的凸包內
                        image[new_y + i, new_x + j] = polygon_cropped[i, j]

            # 將原多邊形區域填充為白色
            cv2.fillPoly(image, [hull], (255, 255, 255))

        # 分別處理左眼、右眼、鼻子和嘴巴
        extract_and_move_polygon(left_eye_points, 10, 10)   # 擷取並移動左眼
        extract_and_move_polygon(right_eye_points, 10, 40)  # 擷取並移動右眼
        extract_and_move_polygon(nose_points, 10, 70)       # 擷取並移動鼻子
        extract_and_move_polygon(mouth_points, 10, 85)      # 擷取並移動嘴巴

    # 保存處理後的圖片
    file_name = os.path.basename(image_path)
    save_path = os.path.join(save_folder, file_name)
    cv2.imwrite(save_path, image)
    print(f"已儲存圖片至: {save_path}")

# 創建新的run資料夾
save_folder = create_run_folder()

# 載入圖像資料
image_path_list = load_data()

# 處理並儲存每張圖像
for image_path in image_path_list:
    process_image(image_path, save_folder)