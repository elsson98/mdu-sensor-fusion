from lidar.rplidar import RPLidar

LiDAR = RPLidar('com7')
LiDAR.stop_motor()
LiDAR.stop()
