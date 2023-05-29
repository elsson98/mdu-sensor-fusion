import cv2
import numpy as np
import open3d

# Initialize camera calibration parameters
camera_calibration_matrix = np.array([[1155.99002568, 0, 1148.63227489], [0, 1160.50098154, 677.39661462], [0, 0, 1]])
distortion_coefficients = np.array([-0.26646883, 0.10383344, 0.00586958, 0.00011171, 0.05510478])


def retrieve_lidar_data():
    # Simulate LiDAR data retrieval from a streaming source
    # Generate a random number of LiDAR points
    num_points = np.random.randint(1000, 5000)

    # Generate random XYZ coordinates for the LiDAR points
    lidar_points_xyz = np.random.rand(num_points, 3) * 10  # Scale by 10 for visualization purposes

    # Generate additional attributes if needed (e.g., intensity, reflectivity)

    return lidar_points_xyz


def retrieve_camera_image():
    # Simulate camera image retrieval from a streaming source
    # In this example, we read an image file for demonstration purposes

    # Read an image file from disk
    camera_image = cv2.imread(
        "camera_calibration/calibration/WIN_20230517_11_08_33_Pro.jpg")  # Replace with the actual retrieval logic

    return camera_image


while True:
    # Retrieve the latest LiDAR point cloud from the streaming source
    lidar_data = retrieve_lidar_data()

    # Retrieve the latest camera image from the streaming source
    camera_image = retrieve_camera_image()

    # Perform LiDAR to camera projection
    lidar_points_xyz = lidar_data[:, :3]
    lidar_points_xy = lidar_data[:, :2]
    camera_points_uv, _ = cv2.projectPoints(lidar_points_xyz, np.zeros((3, 1)), np.zeros((3, 1)),
                                            camera_calibration_matrix, distortion_coefficients)

    # Create a combined point cloud with XYZ and UV coordinates
    combined_cloud = open3d.geometry.PointCloud()
    combined_cloud.points = open3d.utility.Vector3dVector(np.hstack((lidar_points_xyz, camera_points_uv[:, 0, :])))

    # Apply filtering or fusion algorithms to the combined point cloud
    # For example, voxel down-sampling
    voxel_size = 0.02  # Set appropriate size
    downsampled_cloud = combined_cloud.voxel_down_sample(voxel_size)

    # Open3D visualization
    open3d.visualization.draw_geometries([downsampled_cloud])
