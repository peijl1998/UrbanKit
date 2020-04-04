#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
from UrbanUtils.Mongo import Base
from UrbanModels.SI_AGAN import preprocess as SI_AGAN_PREPROCESS
from UrbanModels.SI_AGAN import train as SI_AGAN_TRAIN
import json
import numpy as np



def TrainModel(model_name, data_name, attr_name):
    print(model_name, data_name, attr_name)
    raw_data = []
    items = Base.QueryManyDocument(collection_name=data_name, filter={},
                                   mask={"time": 1, "longitude": 1, "latitude": 1, attr_name: 1})
    print (items)
    if not items:
        return False
    items = json.loads(items)
    for item in items:
        raw_data.append(np.array([item["time"], item["latitude"], item["longitude"], item[attr_name]]))

    raw_data = np.array(raw_data)
    if model_name == "SI-AGAN" or "SI_AGAN":
        SI_AGAN_PREPROCESS.GenerateLowHighPair(raw_data)
        SI_AGAN_TRAIN.run()
        return True
