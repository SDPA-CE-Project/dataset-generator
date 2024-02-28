import cv2
import json
import os

'''
Next image -> keyboard A
Quit -> keyboard Q
'''
folder_path = "image"
jpg_files = [file for file in os.listdir(folder_path) if file.endswith('.jpg')]
jpg_files.sort()
json_files = [file.replace('.jpg', '.json') for file in jpg_files]
current_index = 0

while current_index < len(jpg_files): 
    image_path = os.path.join(folder_path, jpg_files[current_index])
    json_path = os.path.join(folder_path, json_files[current_index])
    image = cv2.imread(image_path)
    try:
        with open(json_path, 'r') as f:
            coordinates = json.load(f)
    except FileNotFoundError:
        continue
        
    for i, coord in enumerate(coordinates, 1):
        x, y = int(coord[0]), int(coord[1])
        cv2.circle(image, (x, y), 1, (0, 255, 0), -1)  
    cv2.namedWindow("Image with points", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image with points", 800, 600)
    cv2.imshow("Image with points", image)
    key = cv2.waitKey(0)
    if key == ord('a'):
        current_index += 1

    elif key == ord('q'):
        break

cv2.destroyAllWindows()