import pandas as pd

CENTER_OF_IMAGE = 2304 / 2


def convert_pixel(row) -> float:
    import math as m
    return m.degrees(m.acos((CENTER_OF_IMAGE - row['center_x']) / CENTER_OF_IMAGE))


if __name__ == "__main__":
    df = pd.read_csv(r"C:\Users\julia\fusion_data\new-raw-data\raw-data\camera_1685451590.csv")
    # df.drop('bb_angle', axis=1)
    # df.drop('filename.1', axis=1)
    df['bounding_box_angle'] = df.apply(convert_pixel, axis=1)
    # df['filename'] = df.apply(lambda x: round(float(x['filename'])), axis=1)
    # df = df.drop_duplicates(subset=['filename'])
    # df['filename'] = df['filename'].unique()
    df.to_csv("camera.csv", index=False)
    print(df)
