#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
import numpy as np
import torch
import math
from torch.autograd import Variable
from UrbanModels.SI_AGAN import preprocess
from UrbanUtils.IO import ConfigReader

config = ConfigReader.GetModelConfig("SI-AGAN")
grid_size = config["grid_size"]
model_output_path = config["model_out_path"]


# data [x,...], x--> [long, lat, value]
def MakeLowData(data):
    low = np.zeros((grid_size, grid_size))
    for item in data:
        i, j = preprocess.GetGridMap(item[0], item[1], grid_size, data)
        low[i][j] = item[2]
    ret = np.zeros((2, grid_size, grid_size))
    ret[0, :, :] = low
    ret[1, :, :] = np.random.rand(grid_size, grid_size)
    return ret


def ModelInference(low):
    model = torch.load(model_output_path)
    model.eval()
    input = Variable(torch.from_numpy(low).float().unsqueeze(0))
    out = model(input).squeeze(0).squeeze(0)
    return out.detach().numpy()


def GetBound(region):
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

    return [min_p[1], max_p[1]], [min_p[0], max_p[0]]


def Predict(data, node=None):
    if not node:
        low = MakeLowData(data)
        out = ModelInference(low)
        r1, r2 = GetBound(data)
        return r1, r2, out
    else:
        data.append([node[0], node[1], 0])
        low = MakeLowData(data)
        out = ModelInference(low)
        i, j = preprocess.GetGridMap(node[0], node[1], grid_size, data)
        return float(out[i][j])
