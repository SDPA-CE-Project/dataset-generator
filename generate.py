import os
import shutil
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from tqdm import tqdm
import json
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates
landmark_indices = [162, 234, 93, 58, 172, 136, 149, 148, 152, 377, 378, 365, 397, 288, 323, 454, 389, 71, 63, 105,
                    66, 107, 336, 296, 334, 293, 301, 168, 197, 5, 4, 75, 97, 2, 326, 305, 33, 160, 158, 133, 153,
                    144, 362, 385, 387, 263, 373, 380, 61, 39, 37, 0, 267, 269, 291, 405, 314, 17, 84, 181, 78, 82,
                    13, 312, 308, 317, 14, 87]


def generateJson(image_path, json_path, del_path, width, height, autoDelete):
  for filename in tqdm(os.listdir(image_path)):
      if filename.endswith(".jpg") or filename.endswith(".png"):
        path = os.path.join(image_path, filename)
        image_origin = cv2.imread(path)
        image_resize = cv2.resize(image_origin, (width, height))

        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_resize)

        detection_result = detector.detect(image)
        #print(detection_result)
        detection_result_list = detection_result.face_landmarks

        if not detection_result_list:
          if autoDelete:
            os.remove(path)
          else:
            shutil.move(path, os.path.join(del_path, filename))
          continue
        cv2.imwrite(path, image_resize)
        landmark_json = []
        for landmarks in detection_result_list:
            for index in landmark_indices:
              landmark_point = landmarks[index]
              landmark_coord = _normalized_to_pixel_coordinates(landmark_point.x, landmark_point.y, width, height)
              landmark_json.append(landmark_coord)
        
        json_file_path = os.path.join(json_path, os.path.splitext(filename)[0] + ".json")
        with open(json_file_path, 'w') as json_file:
          json.dump(landmark_json, json_file)

if __name__ == "__main__":
  #face_landmarker_v2_with_blendshapes.task 모델 경로 설정
  base_options = python.BaseOptions(model_asset_path='/Project/SPDA/faceML/dataset-generator/face_landmarker_v2_with_blendshapes.task')
  ''' 
  Configurations options
  https://developers.google.com/mediapipe/solutions/vision/face_landmarker#configurations_options 
  '''
  options = vision.FaceLandmarkerOptions(base_options=base_options,
                                        output_face_blendshapes=True,
                                        output_facial_transformation_matrixes=True,
                                        num_faces=1)
  detector = vision.FaceLandmarker.create_from_options(options)

  image_path = "./image"
  json_path = "./image"
  del_path = "./delete"
  width = 256
  height = 256

  generateJson(image_path, json_path, del_path, width, height, autoDelete=False)
  '''
    autoDelete -> 얼굴 감지를 실패한 사진을 삭제할지 여부.
                  False로 설정시 사진을 삭제하지 않고 del_path로 옮김.
  '''