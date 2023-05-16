from ultralytics import YOLO

# Load a model
model = YOLO('yolov8x.pt')  # load an official model
# model = YOLO('path/to/best.pt')  # load a custom trained

# Export the model
model.export(format='tflite')
