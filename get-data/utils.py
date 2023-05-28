import math
import shutil
from datetime import datetime
import os
import glob
import pandas as pd


def clean_lidar_data(target_file):
    target_file = target_file + '\\lidar-data.csv'
    df = pd.read_csv(target_file)
    first_second = math.ceil(df['Timestamp'].min())
    last_second = math.floor(df['Timestamp'].max())
    df = df[(df['Timestamp'] >= first_second) & (df['Timestamp'] <= last_second)]
    os.remove(target_file)
    df.to_csv(target_file, index=False)
    print("Removed first and last timestamp from current csv records.")


def create_folders(target):
    dir_path = r'C:\Users\elson\Desktop\mdu-sensor-fusion\raw-data\\' + target
    current_date = datetime.now().strftime('%Y-%m-%d')
    dir_path = dir_path + "\\" + current_date
    day_folder = os.path.join(os.getcwd(), dir_path)
    os.makedirs(day_folder, exist_ok=True)

    current_time = datetime.now().strftime('%H-%M-%S')
    second_folder = os.path.join(day_folder, current_time)
    os.makedirs(second_folder, exist_ok=True)
    return second_folder


def data_consistency_check(image_folder, lidar_csv_file):
    png_dir = image_folder
    png_files = sorted([f for f in os.listdir(png_dir) if f.endswith('.png')])
    first_png_timestamp = png_files[0].rstrip('.png')
    df = pd.read_csv(lidar_csv_file + '\\lidar-data.csv')
    df['Timestamp'] = df['Timestamp'].astype(str)
    if first_png_timestamp in df['Timestamp'].values:
        idx = df[df['Timestamp'] == first_png_timestamp].index[0]
        df = df.iloc[idx:]
    else:
        first_csv_timestamp = df.iloc[0]['Timestamp']
        df = df[df['Timestamp'] != first_csv_timestamp]
    df.to_csv("your_file.csv", index=False)


def cleanup_folders(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def clean_images(target_folder):
    png_files = glob.glob(os.path.join(target_folder, '*.png'))

    if not png_files:
        raise ValueError("No png files found in the directory.")
    basenames = [os.path.splitext(os.path.basename(file))[0] for file in png_files]
    basenames.sort()
    first_second = basenames[0].split('.')[0]
    last_second = basenames[-1].split('.')[0]
    for file in png_files:
        basename = os.path.splitext(os.path.basename(file))[0]
        if basename.startswith(first_second) or basename.startswith(last_second):
            os.remove(file)
    print("Removed first and last timestamp from current frames.")
