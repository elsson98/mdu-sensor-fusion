import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('../processed-data/unique-lidar_1685488062.csv')
    df = df[df['Centroid_X'].notnull()]
    df.to_csv('test.csv', index=False)
    pass