import numpy as np
import cv2
from rplidar import RPLidar
import time

time.sleep(0.3)


def convert_polar_to_cartesian(angles, distance):
    x = distance * np.cos(angles)
    y = distance * -np.sin(angles)
    return x, y


def create_2d_map(x, y, map_size, scale):
    WINDOW_SIZE = (1100, 785)
    img = np.zeros((map_size, map_size, 3), dtype=np.uint8)
    x_img = (x * scale + map_size / 2).astype(int)
    y_img = (y * scale + map_size / 2).astype(int)
    for i in range(len(x_img)):
        cv2.circle(img, (x_img[i], y_img[i]), 2, (255, 0, 0), -1)
    cv2.line(img, (0, map_size // 2), (map_size, map_size // 2), (127, 127, 127), 1)
    cv2.line(img, (map_size // 2, 0), (map_size // 2, map_size), (127, 127, 127), 1)
    img_resized = cv2.resize(img, WINDOW_SIZE, interpolation=cv2.INTER_LINEAR)
    cv2.imshow('2D LiDAR Map from MDU Fusion ', img_resized)
    cv2.waitKey(1)


def lidar_setup():
    scan_counter = 0
    update_rate = 1
    delay = 0.00000001
    map_size = 800
    scale = 80
    rpm = 500
    LiDAR = RPLidar('com7', 115200, 1, None, rpm)
    try:
        print("Starting LiDAR...")
        LiDAR.start_motor()
        for scan in LiDAR.iter_scans():
            print(scan)
            scan_counter += 1
            if scan_counter % update_rate == 0:
                rear_angle_only = [item for item in scan if 0 <= item[1] <= 90 or 270 <= item[1] <= 360]
                angles = np.array([item[1] for item in rear_angle_only]) * np.pi / 180.0
                distance = np.array([item[2] for item in rear_angle_only]) / 1000.0
                y, x = convert_polar_to_cartesian(angles, distance)
                create_2d_map(x, y, map_size, scale)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("Stopping LiDAR...")
    finally:
        LiDAR.reset()
        LiDAR.clear_input()
        LiDAR.stop_motor()
        LiDAR.disconnect()
        LiDAR.__del__()
        cv2.destroyAllWindows()


def main():
    lidar_setup()


if __name__ == '__main__':
    main()
