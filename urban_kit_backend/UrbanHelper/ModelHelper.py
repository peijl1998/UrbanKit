#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
from UrbanUtils.MongoPandas import Base
from UrbanModels.SI_AGAN import preprocess as SI_AGAN_PREPROCESS
from UrbanModels.SI_AGAN import train as SI_AGAN_TRAIN
from UrbanModels.SI_AGAN import predict as SI_AGAN_PREDICT
import pandas as pd


def TrainModel(model_name, data_name, attr_name):
    raw_data = {}
    items = Base.QueryManyDocument(collection_name=data_name, filter={},
                                   mask={"time": 1, "longitude": 1, "latitude": 1, attr_name: 1})
    if not items:
        return False

    for item in items:
        for k in ["time", "latitude", "longitude", attr_name]:
            if k not in item:
                continue
            v = item[k]
            if k in ["latitude", "longitude"]:
                v = float(v)
            if k not in raw_data:
                raw_data[k] = [v]
            else:
                raw_data[k].append(v)

    raw_data = pd.DataFrame.from_dict(raw_data)[["time", "longitude", "latitude", attr_name]].values
    if model_name == "SI-AGAN" or "SI_AGAN":
        SI_AGAN_PREPROCESS.GenerateLowHighPair(raw_data)
        SI_AGAN_TRAIN.run()
        return True


def PredictOne(model_name, longitude, latitude, more):
    if model_name == "SI_AGAN" or model_name == "SI-AGAN":
        return SI_AGAN_PREDICT.Predict(more, [float(longitude), float(latitude)])


def PredictMany(model_name, more):
    if model_name == "SI_AGAN" or model_name == "SI-AGAN":
        r1, r2 ,r3 = SI_AGAN_PREDICT.Predict(more)
        ret = []
        for i in range(r3.shape[0]):
            for j in range(r3.shape[1]):
                jj = r1[0] + (r1[1] - r1[0]) / r3.shape[0] * j
                ii = r2[0] + (r2[1] - r2[0]) / r3.shape[1] * i
                ret.append({"name": "-", "value": [ii, jj, r3[i][j]]})
        return {"lat": r1, "lng": r2, "value": ret, "geo": more}

def PredictMany1(model_name, data, more):
    if model_name == "SI_AGAN" or model_name == "SI-AGAN":
        ret = []
        for i, pos in enumerate(data):
            ret.append([pos[0], pos[1], SI_AGAN_PREDICT.Predict(more, pos)])
            print(ret[-1])
        return ret
