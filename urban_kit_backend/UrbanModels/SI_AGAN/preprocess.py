#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

import numpy as np
import math
from scipy.interpolate import griddata
from UrbanModels.SI_AGAN import utils
from UrbanUtils.IO import ConfigReader
from UrbanUtils.IO import FileUtils

config = ConfigReader.GetModelConfig("SI-AGAN")
low_data_path = config["low_data_path"]
high_data_path = config["high_data_path"]
grid_size = config["grid_size"]
ms_radius = config["mean_shift_radius"]
ms_bandwith = config["mean_shift_bandwith"]
log_path = config["log_path"]

strange_num = -1.2345


def GetGridMap(x, y, size, region):
    min_p = [361, 361]
    max_p = [-1, -1]
    for r in region:
        if r[0] <= min_p[0]:
            min_p[0] = r[0]
        if r[1] <= min_p[1]:
            min_p[1] = r[1]
        if r[0] >= max_p[0]:
            max_p[0] = r[0]
        if r[1] >= max_p[1]:
            max_p[1] = r[1]

    x = math.ceil((size - 1) * (x - min_p[0]) / (max_p[0] - min_p[0]))
    y = math.ceil((size - 1) * (y - min_p[1]) / (max_p[1] - min_p[1]))

    return x, y


# X: (size, 4)  [time, longitude, latitude, value]
def GenerateLowHighPair(X):
    low_quality_data = []
    high_quality_data = []

    # Get The Densest Region
    region_values = X[np.where(X[:, 0] == X[0, 0]), 1:-1][0]
    dense_region = utils.MeanShift(list(region_values[:, :]), radius=ms_radius, bandwidth=ms_bandwith)
    dense_region = region_values[np.array(dense_region)]
    dense_region_key = ["{},{}".format(x[0], x[1]) for x in dense_region]
    FileUtils.WriteFile("MeanShift,Fin\n", log_path, "a")

    # Generate Low and High
    for idx, t in enumerate(np.unique(X[:, 0])):
        FileUtils.WriteFile("Pair,{}\n".format((idx + 1) /len(np.unique(X[:, 0]))), log_path, "a")
        low_z = np.full((grid_size, grid_size), strange_num)
        high_z = np.full((grid_size, grid_size), strange_num)

        # Pad with real value by grid
        site_values = X[np.where(X[:, 0] == t), 1:][0]
        val = {}
        for site in site_values:
            sk = "{},{}".format(site[0], site[1])
            if sk not in dense_region_key:
                continue
            i, j = GetGridMap(site[0], site[1], grid_size, dense_region)
            k = "%d,%d" % (i, j)
            if k in val:
                val[k].append(float(site[2]))
            else:
                val[k] = [float(site[2])]

        for k in val.keys():
            i, j = map(int, k.split(","))
            high_z[i][j] = np.mean(val[k])

        # Random Sample
        low_points = ""
        candidates = list(val.keys())
        already = []
        low_point_num = int(len(candidates) / 4)
        for iter in range(low_point_num):
            flag = True
            k = ""
            while flag:
                k = candidates[np.random.randint(0, len(candidates) - 1)]
                if k not in already:
                    flag = False
            i, j = map(int, k.split(","))
            low_z[i][j] = high_z[i][j]
            high_z[i][j] = strange_num
            low_points += "{},{}\n".format(i, j)

        # Cubic Interpolation
        def interpolation(data):
            points, values, grid = [], [], []
            for i in range(grid_size):
                for j in range(grid_size):
                    grid.append([i, j])
                    if data[i][j] != strange_num:
                        points.append([i, j])
                        values.append(data[i][j])
            points = np.array(points)
            values = np.array(values)
            grid = np.array(grid)

            z = griddata(points, values, grid, method='nearest')
            return z.reshape((grid_size, grid_size))

        try:
            low_z = interpolation(low_z)
            high_z = interpolation(high_z)
        except Exception as e:
            continue

        low_quality_data.append(low_z)
        high_quality_data.append(high_z)
    FileUtils.WriteFile("Pair,Fin\n", log_path, "a")
    low_quality_data = np.array(low_quality_data)
    high_quality_data = np.array(high_quality_data)
    np.save(low_data_path, low_quality_data)
    np.save(high_data_path, high_quality_data)

if __name__ == '__main__':
    pass
