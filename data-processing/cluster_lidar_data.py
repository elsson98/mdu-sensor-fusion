import time
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


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
        if group['New_Spin'].iloc[0] != 'Yes' or len(group) < 2:
            print(f"Skipping group {name} because it has fewer than 2 samples.")
            continue
        angles = np.deg2rad(group['Angle'].values)
        distances = group['Distance'].values
        non_zero_distance_mask = distances != 0
        angles = angles[non_zero_distance_mask]
        distances = distances[non_zero_distance_mask]
        x = distances * np.cos(angles)
        y = distances * np.sin(angles)
        cartesian_coordinates = np.column_stack((x, y))

        if cartesian_coordinates.size == 0:
            print(f"Skipping group {name} because it has no valid (non-zero) distances.")
            continue

        scaler = StandardScaler()
        try:
            scaled_cartesian_coordinates = scaler.fit_transform(cartesian_coordinates)
        except ValueError as e:
            print(f"An error occurred while scaling the coordinates for group {name}: {e}")
            continue

        if len(scaled_cartesian_coordinates) > 0:  # Only perform DBSCAN if there are non-zero distance points
            dbscan = DBSCAN(eps=0.3, min_samples=2)
            dbscan.fit(scaled_cartesian_coordinates)
            labels = np.full(len(group), -1)
            labels[non_zero_distance_mask] = dbscan.labels_
            df.loc[group.index, 'Cluster'] = labels
            mask = dbscan.labels_ != -1
            valid_clusters = scaled_cartesian_coordinates[mask]
            valid_labels = dbscan.labels_[mask]
            unique_labels = np.unique(valid_labels)
            centroids_x = []
            centroids_y = []
            for label in unique_labels:
                if valid_clusters.size > 0 and label in valid_labels:
                    cluster_points = valid_clusters[valid_labels == label]
                    centroid_x = np.mean(cluster_points[:, 0])
                    centroid_y = np.mean(cluster_points[:, 1])
                    centroids_x.append(centroid_x)
                    centroids_y.append(centroid_y)
            if len(centroids_x) > 0:
                unscaled_centroids_x = \
                    scaler.inverse_transform(np.column_stack((centroids_x, np.zeros(len(centroids_x))))).T[0]
                unscaled_centroids_y = \
                    scaler.inverse_transform(np.column_stack((np.zeros(len(centroids_y)), centroids_y))).T[1]
                for i, label in enumerate(unique_labels):
                    centroid_x = unscaled_centroids_x[i]
                    centroid_y = unscaled_centroids_y[i]
                    df.loc[df.index.isin(group.index) & (df['Cluster'] == label), 'Centroid_X'] = centroid_x
                    df.loc[df.index.isin(group.index) & (df['Cluster'] == label), 'Centroid_Y'] = centroid_y
                    plot_clusters(group[non_zero_distance_mask], dbscan.labels_, unscaled_centroids_x,
                                  unscaled_centroids_y)
            else:
                print(f"No centroids were created for group {name}")
    target_path = os.path.join("C:\\Users\\julia\\mdu-fusion-sensor\\processed-data", "lidar_{}".format(str(round(time.time())) + ".csv"))
    # target_path = r'C:\Users\elson\Desktop\mdu-sensor-fusion\processed-data\\' + "lidar-clustered-" + str(
    #     round(time.time())) + ".csv"
    selected_columns = ['Timestamp', 'Angle', 'Distance', 'New_Spin', 'Spin_ID', 'Cluster', 'Centroid_X', 'Centroid_Y']
    df_selected = df[selected_columns]
    df_selected.to_csv(target_path, index=False)
    return target_path


def get_unique_cluster(source_path):
    df = pd.read_csv(source_path)
    unique_spins = df['Spin_ID'].unique()
    dfs = []
    for spin_id in unique_spins:
        df_spin = df[df['Spin_ID'] == spin_id]
        unique_clusters = df_spin['Cluster'].unique()
        for cluster in unique_clusters:
            df_cluster = df_spin[df_spin['Cluster'] == cluster]
            if df_cluster.empty:
                dfs.append(
                    pd.DataFrame({'Spin_ID': [spin_id], 'Cluster': [cluster], 'Centroid_X': [0], 'Centroid_Y': [0]}))
            else:
                df_unique = df_cluster[['Spin_ID', 'Cluster', 'Centroid_X', 'Centroid_Y']].drop_duplicates(
                    subset=['Spin_ID', 'Centroid_X'])
                dfs.append(df_unique)
    df_result = pd.concat(dfs)
    dest_path = source_path.replace('lidar', 'unique-lidar')
    df_result.to_csv(dest_path, index=False)


get_unique_cluster(cluster_data())
