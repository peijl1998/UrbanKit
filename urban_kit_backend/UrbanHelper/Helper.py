#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

from UrbanUtils.IO import ConfigReader
from UrbanUtils.MongoPandas import Base
from UrbanUtils.Math import BaseStat
from UrbanHelper import ModelHelper
import json
import numpy as np


config = ConfigReader.GetConfig()

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)



def GetCollectionLists():
    return list(Base.GetCollectionLists())


def DeleteCollection(name):
    return Base.DeleteCollection(name)


def UploadCsv(file_name, file):
    file = file.split('\r\n')
    try:
        Base.CreateCollection(file_name)
        col_map = {}
        for idx, col in enumerate(file[0].split(',')):
            col_map[idx] = col
        batch_doc = []
        for line in file[1:]:
            doc = {}
            for idx, col in enumerate(line.split(',')):
                doc[col_map[idx]] = col
            batch_doc.append(doc)
        Base.CreateDocumentsInBatch(collection_name=file_name, docs=batch_doc)
        return True
    except Exception as e:
        print("{} save mongo failed. [{}]".format(file_name, str(e)))
        return False


def GetTimeLine(data_name):
    return Base.QueryDistinct(collection_name=data_name, key="time")


def GetAttrList(data_name):
    item = Base.QueryOneDocument(collection_name=data_name)
    if not item:
        return False
    ret = []
    for k in item.keys():
        if k not in ['_id', 'time', 'longitude', 'latitude', 'id']:
            ret.append(k)
    return ret


def GetIdList(data_name):
    return Base.QueryDistinct(data_name, "id")


def GetIdPosition(data_name):
    ids = GetIdList(data_name)
    if not ids:
        return False
    ret = {}
    for id in ids:
        if len(id) == 0:
            continue
        item = Base.QueryOneDocument(collection_name=data_name, filter={"id": id}, mask={"longitude": 1, "latitude": 1})
        longitude = float(item["longitude"])
        latitude = float(item["latitude"])
        ret[id] = [longitude, latitude]
    return ret


# time is represented by idx, not raw format.
def GetAttrByTime(data_name, attr_name, time_step):
    timeline = GetTimeLine(data_name)
    ids = GetIdList(data_name)
    if not ids or time_step > len(timeline) - 1:
        return False
    time_step = timeline[time_step]
    items = Base.QueryManyDocument(collection_name=data_name, filter={'time': time_step}, mask={"id": 1, attr_name: 1})

    ret = []
    for item in items:
        ret.append({'id': item["id"], 'value': float(item[attr_name])})
    return ret


def GetTopAttrByTime(data_name, attr_name, time_step, top):
    attrs = GetAttrByTime(data_name, attr_name, time_step)
    if not attrs:
        return False
    attrs = sorted(attrs, key=lambda d: d['value'], reverse=True)
    tops = []
    vals = []
    for i in range(min(len(attrs), top)):
        tops.append(attrs[i]['id'])
        vals.append(attrs[i]['value'])
    return {'tops': tops, 'vals': vals}


def GetIdStatByTime(data_name, attr_name, time_step, stat_name):
    values = GetAttrByTime(data_name, attr_name, time_step)
    if not values:
        return False
    values = [v["value"] for v in values]
    funcs = {"Q1": BaseStat.Q1, "Mean": BaseStat.Mean, "Q3": BaseStat.Q3,
             "Median": BaseStat.Median, "Min": BaseStat.Min, "Max": BaseStat.Max,
             "Variance": BaseStat.Variance}
    if stat_name not in funcs:
        return False
    return round(funcs[stat_name](values), 2)


def GetAttrById(data_name, attr_name, id):
    items = Base.QueryManyDocument(collection_name=data_name, filter={'id': id}, mask={"time": 1, attr_name: 1})
    if not items:
        return False

    ret = []
    for item in items:
        ret.append({'time': item['time'], 'value': item[attr_name]})

    return ret

def GetMultiAttrById(data_name, attr_names, id):
    if len(attr_names) == 0:
        return True
    items_dict = {}
    timelines = []
    for attr in attr_names:
        items = Base.QueryManyDocument(collection_name=data_name, filter={'id': id}, mask={"time": 1, attr: 1})
        if not items:
            return False
        items_dict[attr] = {}
        temp = []
        for item in items:
            items_dict[attr][item["time"]] = item[attr]
            temp.append(item["time"])

        timelines.append(set(temp))

    timeline = timelines[0]
    if len(timelines) > 1:
        for i in range(1, len(timelines)):
            timeline = timeline & timelines[i]
    timeline = list(timeline)

    ret = []
    for t in timeline:
        v = {}
        for attr in attr_names:
            v[attr] = items_dict[attr][t]
        ret.append({'time': t, 'value': v})

    return ret


def TrainModel(model_name, data_name, attr_name):
    return ModelHelper.TrainModel(model_name, data_name, attr_name)




if __name__ == "__main__":
    # Test Code
    pass
