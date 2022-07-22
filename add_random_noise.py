# Author: J094
# Email: jun.guo.chn@outlook.com
# Date: 2022.07.22
# Description: Create gaussian random noise for EuRoc datasets GroundTruth as gnss simulated data.
#              p_noise: noise for position, unit is meter.
#              q_noise: noise for rotation (euler format), unit is degree.

import csv
from math import degrees
import numpy as np
from scipy.spatial.transform import Rotation


def read_file_list(filename):
    file = open(filename)
    data = file.read()
    lines = data.replace(","," ").replace("\t"," ").split("\n")
    list = [[v.strip() for v in line.split(" ") if v.strip()!=""] for line in lines if len(line)>0 and line[0]!="#"]
    list = [(float(l[0]),l[1:]) for l in list if len(l)>1]
    return dict(list)

def write_list_file(list, filename, p_noise, q_noise):
    with open(filename, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["#timestamp [ns]", "p_RS_R_x [m]", "p_RS_R_y [m]", "p_RS_R_z [m]", "q_RS_w []", "q_RS_x []", "q_RS_y []", "q_RS_z []"])
    for timestamp,line in list.items():
        # Add gaussian noise to p and q.
        # loc: mean, scale: variance, size: dimension
        p = [float(data) for data in line[0:3]]
        # q: x y z w
        q = [float(data) for data in line[4:7]] + [float(line[3])]
        # Creat guassian noise for p and q.
        noise_p = np.random.normal(loc=0.0, scale=p_noise, size=3)
        noise_Eu = np.random.normal(loc=0.0, scale=q_noise, size=3)
        # Add noise to p.
        new_p = p + noise_p
        # Add noise to q.
        Eu = Rotation.from_quat(q).as_euler('xyz', degrees=True)
        new_Eu = Eu + noise_Eu
        # new_q: x y z w
        new_q = Rotation.from_euler('xyz', new_Eu, degrees=True).as_quat()
        # print(new_q)
        line[0:3] = new_p
        # store as w x y z.
        line[3] = new_q[3]
        line[4:7] = new_q[0:3]
        with open(filename, 'a', newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([int(timestamp)]+line[0:7])
    return


if __name__ == "__main__":
    # read and write.
    list = read_file_list("./V101_GT.txt")
    write_list_file(list, "./V101_GT_noise.txt", 5e-3, 5e-1)


