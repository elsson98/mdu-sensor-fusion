import cv2
from PIL import Image
import torch

# Load image
image = Image.open('WIN_20230502_13_47_58_Pro.jpg')

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Run YOLO object detection
results = model(image)

# Extract bounding box information
for r in results.xyxy[0]:
    print(r)
    # left, top, right, bottom = int(x1), int(y1), int(x2), int(y2)
    # print(f'Label: {label}, Confidence: {confidence}, Bounding Box: {left, top, right, bottom}')