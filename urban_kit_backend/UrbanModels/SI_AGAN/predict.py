#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
import numpy as np
import torch
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
    return low


def ModelInference(low):
    model = torch.load(model_output_path)
    out = model(Variable(low))
    return out

def Predict(data, node=None):
    if not node:
        low = MakeLowData(data)
        out = ModelInference(low)
        return out
    else:
        data.append([node[0], node[1], 0])
        low = MakeLowData(data)
        out = ModelInference(low)
        i, j = preprocess.GetGridMap(node[0], node[1], grid_size, data)
        return out[i][j]
