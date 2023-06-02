import pandas as pd

CENTER_OF_IMAGE = 2304 / 2


def convert_pixel(row) -> float:
    import math as m
    return m.degrees(m.atan(row['Centroid_X'] / m.fabs(row['Centroid_Y'])))


if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\julia\mdu-fusion-sensor\data-processing\lidar_distinct.csv")
    # df.drop('bb_angle', axis=1)
    # df.drop('filename.1', axis=1)
    df['cluster_angle'] = df.apply(convert_pixel, axis=1)
    # df['filename'] = df.apply(lambda x: round(float(x['filename'])), axis=1)
    # df = df.drop_duplicates(subset=['filename'])
    # df['filename'] = df['filename'].unique()
    df.to_csv("lidar_with_cluster_angle.csv", index=False)
    print(df)
