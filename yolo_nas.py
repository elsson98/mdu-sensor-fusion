# Load model with pretrained weights
from super_gradients.training import models
from super_gradients.common.object_names import Models

model = models.get(Models.YOLO_NAS_M, pretrained_weights="coco")