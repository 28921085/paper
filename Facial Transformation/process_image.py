import os
import cv2
import dlib
import numpy as np

class ProcessImage:
    def __init__(self, model_path="model/shape_predictor_68_face_landmarks.dat"):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(model_path)

    def draw_entire_face_boundary(self, image, landmarks):
        # 定義整個臉部的特徵點範圍
        entire_face = list(range(0, 68))
        entire_face_pts = np.array([[landmarks.part(p).x, landmarks.part(p).y] for p in entire_face], np.int32)
        entire_face_hull = cv2.convexHull(entire_face_pts)
        cv2.polylines(image, [entire_face_hull], isClosed=True, color=(255, 0, 0), thickness=2)

    def extract_and_move_polygon(self, image, landmarks, points, new_x, new_y):
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
                if mask_cropped[i, j, 0] == 255:
                    image[new_y + i, new_x + j] = polygon_cropped[i, j]

        # 將原多邊形區域填充為白色
        cv2.fillPoly(image, [hull], (255, 255, 255))

    def process_image(self, image_path, save_folder):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        for face in faces:
            landmarks = self.predictor(gray, face)

            # 繪製整個臉部邊界
            self.draw_entire_face_boundary(image, landmarks)

            # 定義眼睛、鼻子和嘴巴的特徵點範圍
            left_eye_points = list(range(36, 42))  # 左眼
            right_eye_points = list(range(42, 48))  # 右眼
            nose_points = list(range(27, 36))  # 鼻子
            mouth_points = list(range(48, 68))  # 嘴巴

            # 分別處理左眼、右眼、鼻子和嘴巴
            self.extract_and_move_polygon(image, landmarks, left_eye_points, 10, 10)
            self.extract_and_move_polygon(image, landmarks, right_eye_points, 10, 40)
            self.extract_and_move_polygon(image, landmarks, nose_points, 10, 70)
            self.extract_and_move_polygon(image, landmarks, mouth_points, 10, 85)

        # 保存處理後的圖片
        file_name = os.path.basename(image_path)
        save_path = os.path.join(save_folder, file_name)
        cv2.imwrite(save_path, image)
        print(f"已儲存圖片至: {save_path}")
