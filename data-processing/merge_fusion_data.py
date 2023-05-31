import pandas as pd
import os
import numpy as np

if __name__ == "__main__":
    lidar_df = pd.read_csv('lidar_with_cluster_angle.csv')
    # df = df[df['Centroid_X'] > 0]
    # df.to_csv('lidar_distinct.csv', index=False)
    image_data = []
    with open("camera.csv", 'r') as cameri:
        lines = cameri.readlines()
        for folder in os.listdir(r"C:\Users\julia\fusion_data\new-raw-data\raw-data\camera-data\2023-05-30"):
            file = os.listdir(os.path.join(r"C:\Users\julia\fusion_data\new-raw-data\raw-data\camera-data\2023-05-30"
                                           , folder))[0]
            for line in lines:
                # print(line, end="")
                print(file, end="")
                if file.split(".")[0] in line:
                    values = [val.strip() for val in line.split(",")]
                    image_data.append([values[5], values[6], values[8]])
            # 5 6 8
    data = np.array(image_data)
    print(data)
    image_df = pd.DataFrame(data=data, columns=['center_x', 'center_y', 'bounding_box_angle'])
    merged = lidar_df.merge(image_df, left_index=True, right_index=True, how='inner')\
        .to_csv("training_data.csv", index=False)
