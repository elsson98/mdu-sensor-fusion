import cv2
import numpy as np
from PIL import Image
# import torch
#
# # Load image
# image = Image.open('WIN_20230502_13_47_58_Pro.jpg')
#
# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#
# # Run YOLO object detection
# results = model(image)
#
# # Convert image to OpenCV format
# image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#
# # Loop through detections and draw bounding boxes
# for label, confidence, (x1, y1, x2, y2) in results.xyxy[0]:
#     left, top, right, bottom = int(x1), int(y1), int(x2), int(y2)
#     cv2.rectangle(image_cv, (left, top), (right, bottom), (0, 255, 0), 2)
#     cv2.putText(image_cv, f'{label} {confidence:.2f}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
#
# # Show image with bounding boxes
# cv2.imshow('Image', image_cv)
# cv2.waitKey(0)

import torch
from PIL import Image
from pathlib import Path

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov8', 'custom', path=Path('yolov8s.pt'))

# Load the input image
image = Image.open('WIN_20230502_13_47_58_Pro.jpg')

# Perform object detection
results = model(image)

# Extract the coordinates
for detection in results.xyxy[0]:
    x1, y1, x2, y2, confidence, class_id = detection
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    width = x2 - x1
    height = y2 - y1
    print(f"Class ID: {class_id}, Coordinates: ({x1}, {y1}, {width}, {height})")