import os
import cv2
import dlib
import numpy as np
import random

class ProcessImage:
    def __init__(self, model_path="model/shape_predictor_68_face_landmarks.dat"):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(model_path)

    def draw_entire_face_boundary(self, image, landmarks):
        entire_face = list(range(0, 68))
        entire_face_pts = np.array([[landmarks.part(p).x, landmarks.part(p).y] for p in entire_face], np.int32)
        entire_face_hull = cv2.convexHull(entire_face_pts)
        #畫臉部邊界
        #cv2.polylines(image, [entire_face_hull], isClosed=True, color=(255, 0, 0), thickness=2)
        return entire_face_hull  # 返回整個臉部的凸包

    def extract_polygons(self, image, landmarks, points):
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

        return polygon_cropped, mask_cropped, hull  # 返回五官的圖像區域、遮罩、和凸包

    def move_polygon(self, image, polygon_cropped, mask_cropped, entire_face_hull):
        # 隨機生成在臉部凸包內的新位置
        valid_position = False
        while not valid_position:
            offset_y = random.randint(0, image.shape[0] - polygon_cropped.shape[0])
            offset_x = random.randint(0, image.shape[1] - polygon_cropped.shape[1])

            # 檢查隨機位置是否在臉部凸包內
            if cv2.pointPolygonTest(entire_face_hull, (offset_x + polygon_cropped.shape[1] // 2, 
                                                       offset_y + polygon_cropped.shape[0] // 2), False) >= 0:
                valid_position = True

        # 使用for迴圈將多邊形範圍內的像素移動到新位置，並添加條件檢查
        for i in range(polygon_cropped.shape[0]):
            for j in range(polygon_cropped.shape[1]):
                if mask_cropped[i, j, 0] == 255:
                    target_x, target_y = offset_x + j, offset_y + i
                    if cv2.pointPolygonTest(entire_face_hull, (target_x, target_y), False) >= 0:
                        image[target_y, target_x] = polygon_cropped[i, j]

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        for face in faces:
            landmarks = self.predictor(gray, face)

            # 繪製整個臉部邊界並獲取凸包
            entire_face_hull = self.draw_entire_face_boundary(image, landmarks)

            # 定義眼睛、鼻子和嘴巴的特徵點範圍
            facial_features = {
                "left_eye": list(range(36, 42)),
                "right_eye": list(range(42, 48)),
                "nose": list(range(27, 36)),
                "mouth": list(range(48, 68))
            }

            # Step 1: 提取所有五官的區域
            extracted_features = {}
            for feature, points in facial_features.items():
                extracted_features[feature] = self.extract_polygons(image, landmarks, points)

            # Step 2: 填充所有五官的區域為白色
            for _, (_, _, hull) in extracted_features.items():
                cv2.fillPoly(image, [hull], (255, 255, 255))

            # Step 3: 隨機移動每個五官區域
            for _, (polygon_cropped, mask_cropped, _) in extracted_features.items():
                self.move_polygon(image, polygon_cropped, mask_cropped, entire_face_hull)

        return image
    