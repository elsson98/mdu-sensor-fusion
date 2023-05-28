from rplidar import RPLidar

PORT_NAME = 'COM7'

lidar = RPLidar(PORT_NAME, rpm=100)
print(lidar.get_info())
try:
    for measurement in lidar.iter_measurments():
        print(measurement)

except KeyboardInterrupt:
    print('Stoping...')
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
