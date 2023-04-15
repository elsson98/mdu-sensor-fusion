from ultralytics import YOLO
import logging

model = YOLO("yolov8x.pt")
results = model.predict(source="0", show=True, stream=True)
for r in results:
    logging.log(0, r.boxes, r.masks, r.probs)
