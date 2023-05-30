import matplotlib.pyplot as plt
import numpy as np


def read_data():
    with open("../resources/sample-data.txt", 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split(" ")
            x.append(float(p[0]))
            y.append(float(p[1]))
    return x, y


angle, distance = read_data()
plt.scatter(np.array(angle), np.array(distance))
plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('LIDAR map from Fusion Team')
plt.show()
