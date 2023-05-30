import csv
import math as m
import os
import time

from ultralytics import YOLO

model = YOLO("../yolo/yolov8x.pt")

dir_path = r"C:\Users\elson\Desktop\mdu-sensor-fusion\raw-data\merged-data\all-images"
csv_path = r"C:\Users\elson\Desktop\mdu-sensor-fusion\processed-data\\" + "camera-bb-cxy" + str(round(time.time())) + ".csv"
image_width = 640
with open(csv_path, 'w', newline='') as csvfile:
    fieldnames = ['filename', 'x', 'y', 'x2', 'y2', 'center_x', 'center_y', 'bb_angle', 'class']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    count = 0
    filenames = os.listdir(dir_path)
    filenames.sort(reverse=True)
    for file_name in filenames:
        file_path = os.path.join(dir_path, file_name)
        results = model.predict(source=file_path, project="processed-data-yolo", name="yolo", save=True)
        result = results[0]
        box = result.boxes[0]
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        x, y, x2, y2 = cords
        center_x = (x + x2) / 2
        center_y = (y + y2) / 2
        bb_angle = m.acos((image_width - y) / image_width) * (180 / m.pi)
        if class_id == 'person':
            count += 1
            print(f"Processing image : {file_name.replace('.png', '')} number of image {count}")
            writer.writerow(
                {'filename': file_name.replace('.png', ''), 'x': x, 'y': y, 'x2': x2, 'y2': y2, 'center_x': center_x,
                 'center_y': center_y, 'bb_angle': bb_angle, 'class': class_id})
        else:
            print("Box doesn't contain person")
            writer.writerow(
                {'filename': file_name.replace('.png', ''), 'x': 0, 'y': 0, 'x2': 0, 'y2': 0, 'center_x': 0,
                 'center_y': 0, 'bb_angle': 0, 'class': "No Data"})
