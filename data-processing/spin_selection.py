import os
import sys

if __name__ == '__main__':
    for capture in os.listdir("C:/Users/julia/fusion_data/new-raw-data/raw-data/lidar-data/2023-05-30"):
        csv_folder = os.listdir("C:/Users/julia/fusion_data/new-raw-data/raw-data/lidar-data/2023-05-30/" + capture)
        print(csv_folder[0])
        # csv_file = os.listdir("new-raw-data/raw-data/lidar-data/2023-05-30/" + capture + "/" + folder)[0]
        with open("C:/Users/julia/fusion_data/new-raw-data/raw-data/lidar-data/2023-05-30/" + capture + "/reduced_spins.csv", 'w',
                  encoding="utf-8") as sink:
            sink.write("Timestamp,Angle,Distance,New_Spin\n")
            with open("C:/Users/julia/fusion_data/new-raw-data/raw-data/lidar-data/2023-05-30/" + capture + "/" +
                      csv_folder[0], "r") as data:
                i = 0
                lines = data.readlines()
                for row in lines:
                    print(row, end="")
                    if "Yes" in row:
                        i = i + 1
                    if i == 1 or i == 2:
                        sink.write(row)
                    if i == 2:
                        break
        import pandas as pd

        df = pd.read_csv(
            "C:/Users/julia/fusion_data/new-raw-data/raw-data/lidar-data/2023-05-30/" + capture + "/reduced_spins.csv")
        df = df.tail(-1)
        df.to_csv(
            "C:/Users/julia/fusion_data/new-raw-data/raw-data/lidar-data/2023-05-30/" + capture + "/reduced_spins.csv",
            index=False)
