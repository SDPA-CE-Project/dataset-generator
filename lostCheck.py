import os
import shutil
from tqdm import tqdm

#탐색할 경로
source_folder = "celeb/cropped"
#손실파일 옮길 경로
destination_folder = "celeb/loss"

files = os.listdir(source_folder)

jpg_files = [f for f in files if f.endswith('.jpg')]
json_files = [f for f in files if f.endswith('.json')]

print("Check JSON loss")
for jpg_file in tqdm(jpg_files):
    json_file = f"{os.path.splitext(jpg_file)[0]}.json"
    if json_file not in json_files:
        print(f"JSON Loss | JPG: {jpg_file}")
        shutil.move(os.path.join(source_folder, jpg_file), os.path.join(destination_folder, jpg_file))
print("Check finish")
        
print("Check JPG loss")
for json_file in tqdm(json_files):
    jpg_file = f"{os.path.splitext(json_file)[0]}.jpg"
    if jpg_file not in jpg_files:
        print(f"JPG Loss | JSON: {json_file}")
        shutil.move(os.path.join(source_folder, json_file), os.path.join(destination_folder, json_file))
print("Check finish")
