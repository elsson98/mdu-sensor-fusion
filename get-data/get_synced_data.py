import csv
import multiprocessing
import time

import cv2

from rplidar import RPLidar, RPLidarException
from utils import *


def camera_data(start_event, exception_event):
    dir_path = create_folders('camera-data')
    cap = cv2.VideoCapture(1)
    start_event.set()
    target_fps = 16
    try:
        frame_count = 0
        print("Camera started at : " + str(time.time()))
        time.sleep(4)
        print("Grabing data")
        while True:
            if exception_event.is_set():
                break
            start_time = time.time()
            for _ in range(target_fps):
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite(os.path.join(dir_path, '{}.png'.format(time.time())), frame)
                    frame_count += 1
                else:
                    break
            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < 1.0:
                time.sleep(1.0 - elapsed_time)
    except KeyboardInterrupt as ex:
        print(f"Stopping camera due to {type(ex).__name__} at : {time.time()}")
        clean_images(dir_path)
        if isinstance(ex, KeyboardInterrupt):
            exception_event.set()
    except Exception as e:
        print(f"Stopping camera due to {type(e).__name__} at : {time.time()}")
        if isinstance(e, Exception):
            exception_event.set()
    finally:
        cap.release()


def read_lidar_data(start_event, exception_event):
    lidar = None
    output_file = create_folders('lidar-data')
    try:
        start_event.wait()
        lidar = RPLidar('com7', rpm=770)
        print('LiDAR started at: ' + str(time.time()))
        with open(output_file + '\\lidar-data.csv', 'w', newline='') as output_file_csv:
            csv_writer = csv.writer(output_file_csv)
            csv_writer.writerow(["Timestamp", "Angle", "Distance", "New_Spin"])
            last_angle = -1
            time.sleep(4.9)
            print("Grabbing data, stop at least after 3s to have data...")
            for i, measurement in enumerate(lidar.iter_measurments()):
                timestamp = time.time()
                if exception_event.is_set():
                    break
                scan, quality, angle, distance = measurement
                if last_angle - 10 > angle:
                    new_spin = 'Yes'
                else:
                    new_spin = 'No'
                last_angle = angle
                if 0 <= angle <= 59 or 301 <= angle <= 360:
                    csv_writer.writerow([timestamp, angle, distance, new_spin])
    except RPLidarException as ex:
        print(f"Stopping LiDAR due to {type(ex).__name__} at: {time.time()}")
        cleanup_folders(output_file)
        cleanup_folders(output_file.replace('lidar', 'camera'))
        print("One of the sensors failed to start deleting created folder...")
        exception_event.set()
    except KeyboardInterrupt as e:
        output_file_csv.close()
        clean_lidar_data(output_file)
        # This function is not completed yet
        # data_consistency_check(output_file.replace('lidar', 'camera'), output_file)
        print(f"Stopping LiDAR due to {type(e).__name__} at: {time.time()}")
        if not isinstance(e, KeyboardInterrupt):
            exception_event.set()
    finally:
        if lidar:
            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()


if __name__ == "__main__":
    try:
        start_event = multiprocessing.Event()
        exception_event = multiprocessing.Event()
        process1 = multiprocessing.Process(target=read_lidar_data, args=(start_event, exception_event,))
        process2 = multiprocessing.Process(target=camera_data, args=(start_event, exception_event,))
        process2.start()
        process1.start()

        while True:
            if exception_event.is_set():
                process1.terminate()
                process2.terminate()
                break

            if not process1.is_alive() and not process2.is_alive():
                break

            time.sleep(1)
    except Exception:
        print("Stopping due to keyboard interrupt")
        process1.terminate()
        process2.terminate()
