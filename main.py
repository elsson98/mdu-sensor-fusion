import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image as im

import logging

model = YOLO("yolov8x.pt")
results = model.predict(source="WIN_20230508_11_06_59_Pro.jpg")
results = model.fuse()

# res_plotted = results[0].boxes.plot()
# print(res_plotted)
# # cv2.imwrite('prediction.jpg', res_plotted)
# cv2.imshow("result", res_plotted)
# cv2.waitKey(0)

x = results[0].boxes.shape[0]
y = results[0].boxes.shape[1]
img = np.full((1296, 2304, 3), 255, dtype=np.uint8)
image = im.fromarray(img)


def fill_row(df, y, x1, x2):
    for rgb in range(x1, x2):
        df[rgb][y] = [0, 0, 128]
        # df[rgb][y + 1] = [0, 0, 128]
        # df[rgb][y - 1] = [0, 0, 128]


def fill_column(df, x, y1, y2):
    for rgb in range(y1, y2):
        df[x][rgb] = [0, 0, 128]
        # df[x + 1][rgb] = [0, 0, 128]
        # df[x - 1][rgb] = [0, 0, 128]


# print(img)
for r in results:
    # TODO
    # image shape x = 2304 and y = 1296
    for box in r.boxes:
        print(box.xyxy)
        xyxy = box.xyxy
        print(box)
        x1 = int(xyxy[0][0])
        y1 = int(xyxy[0][1])
        x2 = int(xyxy[0][2])
        y2 = int(xyxy[0][3])

        fill_column(img, y1, x1, x2)
        fill_column(img, y2, x1, x2)
        fill_row(img, x1, y1, y2)
        fill_row(img, x2, y1, y2)

image = im.fromarray(img)
image.save("test.jpg")
