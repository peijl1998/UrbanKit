#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
# This file provide something useful for SI-AGAN Model.
import numpy as np
import math
import os
from geopy.distance import geodesic
from torch.utils.data import Dataset
from UrbanUtils.IO import ConfigReader

config = ConfigReader.GetModelConfig("SI-AGAN")
low_data_path = config["low_data_path"]  # data_root + "low_data.npy"
high_data_path = config["high_data_path"]  # data_root + "high_data.npy"


def SpatialDistance(x1, x2):
    return geodesic((x1[1], x1[0]), (x2[1], x2[0])).km


def GetMeanPos(X):
    return np.mean(np.array(X), axis=0)


# Find the densest region by mean-shift algorithm
def MeanShift(X, radius=5, bandwidth=25, n_iterations=100):
    def neighbourhood_points(X, x_centroid):
        eligible_X = []
        for x in X:
            distance_between = SpatialDistance(x, x_centroid)
            if distance_between <= radius:
                eligible_X.append(x)
        return eligible_X

    def neighbourhood_points_idx(X, x_centroid):
        eligible_X = []
        for i in range(len(X)):
            x = X[i]
            distance_between = SpatialDistance(x, x_centroid)
            if distance_between <= radius:
                eligible_X.append(i)
        return eligible_X

    def gaussian_kernel(distance, bandwidth):
        val = (1 / (bandwidth * math.sqrt(2 * math.pi))) * np.exp(-0.5 * ((distance / bandwidth)) ** 2)
        return val

    cnt = GetMeanPos(X)
    for it in range(n_iterations):
        neighbours = neighbourhood_points(X, cnt)

        numerator = 0.
        denominator = 0.
        for neighbour in neighbours:
            distance = SpatialDistance(neighbour, cnt)
            weight = gaussian_kernel(distance, bandwidth)
            numerator += (weight * neighbour)
            denominator += weight
        new_x = numerator / denominator

        cnt = new_x

    return neighbourhood_points_idx(X, cnt)


def GetData(path, res):
    assert res == "high" or res == "low"
    if res == "high":
        data = np.load(path).astype("float").tolist()
        matrix_size = len(data[0])
        ret = []
        for arr in data:
            new_arr = np.zeros((matrix_size, matrix_size, 1))
            new_arr[:, :, 0] = arr
            ret.append(np.array(new_arr))
        return ret

    if res == "low":
        data = np.load(path).astype("float").tolist()
        matrix_size = len(data[0])
        real_low_points = [[x, y] for x in range(matrix_size) for y in range(matrix_size)]

        def distance(p1, p2):
            return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        def normalize(data):
            mx = np.max(data)
            mn = np.min(data)
            [rows, cols] = data.shape
            for i in range(rows):
                for j in range(cols):
                    data[i, j] = (data[i, j] - mn) / (mx - mn)
            return data

        site_map = np.zeros((matrix_size, matrix_size))
        for p in real_low_points:
            d_max = max(distance(p, [0, matrix_size - 1]), distance(p, [matrix_size - 1, matrix_size - 1]),
                        distance(p, [matrix_size - 1, 0]), distance(p, [0, 0]))
            beta = 0.6

            z = np.zeros((matrix_size, matrix_size))
            for i in range(matrix_size):
                for j in range(matrix_size):
                    z[i][j] = math.pow(distance(p, [i, j]), beta) / math.pow(d_max, beta)

            site_map += z

        site_map = normalize(site_map)

        ret = []
        for arr in data:
            new_arr = np.zeros((matrix_size, matrix_size, 2))
            new_arr[:, :, 0] = arr
            new_arr[:, :, 1] = site_map
            ret.append(new_arr)
        return ret


class MyDataset(Dataset):
    def __init__(self):
        high_res_real = GetData(high_data_path, 'high')
        low_res = GetData(low_data_path, 'low')

        self.data = low_res
        self.label = high_res_real

    def __getitem__(self, idx):
        return self.data[idx], self.label[idx]

    def __len__(self):
        return len(self.data)
