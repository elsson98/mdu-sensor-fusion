import time
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_clusters(group, labels, centroids_x, centroids_y):
    angles = np.deg2rad(group['Angle'].values)
    distances = group['Distance'].values
    spin_name = group['Spin_ID'].iloc[0]
    plt.figure(figsize=(6, 6))
    plt.subplot(projection='polar')
    scatter = plt.scatter(angles, distances, c=labels, cmap='viridis', alpha=1)
    centroid_angles = np.arctan2(centroids_y, centroids_x)
    centroid_angles = np.rad2deg(centroid_angles)
    centroid_angles = (centroid_angles + 360) % 360
    centroid_distances = np.sqrt(np.array(centroids_x) ** 2 + np.array(centroids_y) ** 2)
    centroid_scatter = plt.scatter(np.deg2rad(centroid_angles), centroid_distances, c='red', s=20)
    for i, (angle, dist) in enumerate(zip(centroid_angles, centroid_distances)):
        plt.annotate(str(i), (np.deg2rad(angle), dist))

    plt.title(f'Spin: {spin_name}')
    dir_name = r'C:\Users\julia\fusion_data\new-raw-data\raw-data\merged-data\clustered_data_visualization'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    plt.savefig(f'{dir_name}\\spin_{spin_name}.jpg')
    plt.show()
    plt.close()


def cluster_data():
    df = pd.read_csv("C:\\Users\\julia\\fusion_data\\new-raw-data\\raw-data\\merged-data\\all-lidar-data-1685476159.csv")
    df['New_Spin_Flag'] = np.where(df['New_Spin'] == 'Yes', 1, 0)
    df['Spin_ID'] = df['New_Spin_Flag'].cumsum()
    df['Centroid_X'] = np.nan
    df['Centroid_Y'] = np.nan

    groups = df.groupby('Spin_ID')
    for name, group in groups:
        if group['New_Spin'].iloc[0] != 'Yes':
            continue
        angles = np.deg2rad(group['Angle'].values)
        distances = group['Distance'].values
        if len(angles) < 3:
            print(f"Skipping group {name} because it has fewer than 3 samples.")
            continue
        x = distances * np.cos(angles)
        y = distances * np.sin(angles)
        cartesian_coordinates = np.column_stack((x, y))
        scaler = StandardScaler()
        scaled_cartesian_coordinates = scaler.fit_transform(cartesian_coordinates)
        dbscan = DBSCAN(eps=0.45, min_samples=2)
        dbscan.fit(scaled_cartesian_coordinates)
        df.loc[group.index, 'Cluster'] = dbscan.labels_
        mask = dbscan.labels_ != -1
        valid_clusters = scaled_cartesian_coordinates[mask]
        valid_labels = dbscan.labels_[mask]
        unique_labels = np.unique(valid_labels)
        centroids_x = []
        centroids_y = []
        for label in unique_labels:
            cluster_points = valid_clusters[valid_labels == label]
            centroid_x = np.mean(cluster_points[:, 0])
            centroid_y = np.mean(cluster_points[:, 1])
            centroids_x.append(centroid_x)
            centroids_y.append(centroid_y)
        unscaled_centroids_x = scaler.inverse_transform(np.column_stack((centroids_x, np.zeros(len(centroids_x))))).T[0]
        unscaled_centroids_y = scaler.inverse_transform(np.column_stack((np.zeros(len(centroids_y)), centroids_y))).T[1]
        for i, label in enumerate(unique_labels):
            centroid_x = unscaled_centroids_x[i]
            centroid_y = unscaled_centroids_y[i]
            df.loc[df.index.isin(group.index) & (df['Cluster'] == label), 'Centroid_X'] = centroid_x
            df.loc[df.index.isin(group.index) & (df['Cluster'] == label), 'Centroid_Y'] = centroid_y
            plot_clusters(group, dbscan.labels_, unscaled_centroids_x, unscaled_centroids_y)
    target_path = os.path.join("C:\\Users\\julia\\mdu-fusion-sensor\\processed-data", "lidar_{}".format(str(round(time.time())) + ".csv"))
    # target_path = r'./processed-data\\' + "lidar_" + str(
    #     round(time.time())) + ".csv"
    selected_columns = ['Timestamp', 'Angle', 'Distance', 'New_Spin', 'Spin_ID', 'Cluster', 'Centroid_X', 'Centroid_Y']
    df_selected = df[selected_columns]
    df_selected.to_csv(target_path, index=False)
    return target_path


def get_unique_cluster(source_path):
    df = pd.read_csv(source_path)
    df = df[df['Cluster'] == 1]
    df = df[['Spin_ID', 'Cluster', 'Centroid_X', 'Centroid_Y']]
    df = df.drop_duplicates(subset=['Spin_ID', 'Centroid_X'])
    dest_path = source_path.replace('lidar', 'unique-cluster-lidar')
    df.to_csv(dest_path, index=False)


path = cluster_data()
get_unique_cluster(path)
