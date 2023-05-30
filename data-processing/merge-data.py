import os
import shutil

import pandas as pd


def copy_images_with_timestamp(source_dir, dest_dir_base):
    png_file_exists = False
    if not os.path.exists(dest_dir_base):
        os.makedirs(dest_dir_base)
    for foldername, subfolders, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.lower().endswith('.png'):
                png_file_exists = True
                source_file = os.path.join(foldername, filename)
                dest_file = os.path.join(dest_dir_base, filename)
                shutil.copy2(source_file, dest_file)
    if png_file_exists:
        print("All PNG files have been copied.")
    else:
        print("No PNG files were found to copy.")


def merge_csv_files(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dfs = []
    csv_file_exists = False
    for foldername, subfolders, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.lower() == 'reduced_spins.csv':
                csv_file_exists = True
                source_file = os.path.join(foldername, filename)
                df = pd.read_csv(source_file)
                dfs.append(df)
    if csv_file_exists:
        merged_df = pd.concat(dfs, ignore_index=True)
        new_filename = f"all-lidar.csv"
        dest_file = os.path.join(dest_dir, new_filename)
        merged_df.to_csv(dest_file, index=False)
        print("All CSV files have been merged.")
    else:
        print("No CSV files were found to merge.")


image_source_dir = r'C:\Users\elson\Desktop\mdu-sensor-fusion\raw-data\camera-data'
image_dest_dir_base = r'C:\Users\elson\Desktop\mdu-sensor-fusion\raw-data\merged-data\all-images'
csv_source_dir = r'C:\Users\julia\fusion_data\new-raw-data\raw-data\lidar-data'
csv_dest_dir = r'C:\Users\julia\fusion_data\new-raw-data\raw-data\merged-data'

# copy_images_with_timestamp(image_source_dir, image_dest_dir_base)
merge_csv_files(csv_source_dir, csv_dest_dir)
