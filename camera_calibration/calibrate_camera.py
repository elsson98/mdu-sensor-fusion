import glob

import cv2
import numpy as np
np.set_printoptions(suppress=True)

# Set the number of chessboard corners
num_corners_x = 7
num_corners_y = 7

# Set the size of the chessboard squares in meters
square_size = 0.035

# Prepare object points, e.g., (0,0,0), (1,0,0), (2,0,0), ..., (8,5,0)
object_points = np.zeros((num_corners_x * num_corners_y, 3), np.float32)
object_points[:,:2] = np.mgrid[0:num_corners_x, 0:num_corners_y].T.reshape(-1, 2) * square_size

# Arrays to store object points and image points from calibration images
object_points_list = []   # 3D points in real world space
image_points_list = []    # 2D points in image plane

# Read calibration images and detect chessboard corners
calibration_images = glob.glob('calibration/*.jpg')  # Adjust the path to your calibration image directory
print(len(calibration_images))
for image_path in calibration_images:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (num_corners_x, num_corners_y), None)
    # If corners are found, add object points and image points
    if ret:
        object_points_list.append(object_points)
        image_points_list.append(corners)

# Perform camera calibration
ret, camera_matrix, distortion_coeffs, _, _ = cv2.calibrateCamera(object_points_list, image_points_list, gray.shape[::-1], None, None)

# Print the camera calibration matrix
print("Camera Calibration Matrix:")
print(camera_matrix)
print(distortion_coeffs)
