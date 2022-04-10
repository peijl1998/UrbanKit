#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
from django.http import HttpResponse

from UrbanUtils.IO import ConfigReader, FileUtils
#from UrbanUtils.MongoPandas import Base
from UrbanUtils.Mongo import Base
from UrbanUtils.Math import BaseStat
from UrbanHelper import ModelHelper
import json
import numpy as np

config = ConfigReader.GetConfig()
last_p = 0

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


def UploadModel(file_name, file):
    try:
        FileUtils.WriteFile(file, ConfigReader.GetModelConfig(file_name), "wb")
        return True
    except Exception as e:
        print("{} save mongo failed. [{}]".format(file_name, str(e)))
        return False



def GetTimeLine(data_name):
    ret = []
    for t in Base.QueryDistinct(collection_name=data_name, key="time"):
        if t != None:
            ret.append(t)
    return ret


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


from scipy.stats import pearsonr
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
def CalCorr(data_name, attr_names, id, method):
    raw = GetMultiAttrById(data_name, attr_names, id)
    raw = sorted(raw, key=lambda x:x["time"])

    ts = {}
    for a in attr_names:
        ts[a] = []

    for t in raw:
        for a in attr_names:
            ts[a].append(t["value"][a])

    ret = []
    record = {}
    for a1 in attr_names:
        for a2 in attr_names:
            if a1 not in record:
                record[a1] = {}
            if a2 not in record:
                record[a2] = {}
            l1 = np.array(ts[a1])
            l2 = np.array(ts[a2])
            if method == 'DTW':
                if a2 in record[a1]:
                    d = record[a1][a2]
                elif a1 in record[a2]:
                    d = record[a2][a1]
                else:
                    d, _ = fastdtw(l1, l2, dist=euclidean)
                    record[a1][a2] = d
                    print(a1, a2)
                ret.append([a1, a2, np.round(d)])
            elif method == "Pearson":
                d = np.round(pearsonr(l1, l2)[0], 3)
                ret.append([a1, a2, d])

    return ret

def TrainModel(model_name, data_name, attr_name):
    RemoveLog(model_name)
    return ModelHelper.TrainModel(model_name, data_name, attr_name)


def PredictOne(model_name, data_name, longitude, latitude, time_step, attr_name):
    id_pos = GetIdPosition(data_name)
    id_val_list = GetAttrByTime(data_name, attr_name, time_step)
    id_val = {}
    for item in id_val_list:
        id_val[item["id"]] = item["value"]
    more = []
    for k in id_pos:
        if k not in id_val:
            continue
        more.append(id_pos[k] + [id_val[k]])
    return ModelHelper.PredictOne(model_name, longitude, latitude, more)


def PredictMany(model_name, data_name, time_step, attr_name):
    id_pos = GetIdPosition(data_name)
    id_val_list = GetAttrByTime(data_name, attr_name, time_step)
    id_val = {}
    for item in id_val_list:
        id_val[item["id"]] = item["value"]
    more = []
    for k in id_pos:
        if k not in id_val:
            continue
        more.append(id_pos[k] + [id_val[k]])
    return ModelHelper.PredictMany(model_name, more)


def PredictMany1(model_name, data_name, time_step, attr_name):
    id_pos = GetIdPosition(data_name)
    id_val_list = GetAttrByTime(data_name, attr_name, time_step)
    id_val = {}
    for item in id_val_list:
        id_val[item["id"]] = item["value"]
    more = []
    for k in id_pos:
        more.append(id_pos[k] + [id_val[k]])

    def get_bound(region, size=20):
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

        ret = []
        x_gap = (max_p[0] - min_p[0]) / size
        y_gap = (max_p[1] - min_p[1]) / size
        for i in range(size):
            for j in range(size):
                ret.append([min_p[0] + x_gap * i, min_p[1] + y_gap * j])

        return ret

    aug_data = get_bound(more)

    return ModelHelper.PredictMany1(model_name, aug_data, more)


def RemoveLog(model_name):
    global last_p
    last_p = 0
    FileUtils.DeleteFile(ConfigReader.GetModelConfig(model_name)["log_path"])

def GetTrainProgress(model_name):
    global last_p
    latest_log = FileUtils.ReadFile(ConfigReader.GetModelConfig(model_name)["log_path"])
    if not latest_log or len(latest_log) == 0 or len(latest_log[-1].split(",")) != 2:
        return last_p
    latest_log = latest_log[-1].split(',')
    s1, s2 = latest_log[0], latest_log[1]
    p = 0
    if s1 == "MeanShift":
        p = min(10, last_p + 1)
    if s1 == "Pair":
        if s2 == "Fin":
            p = 40
        else:
            p = 10 + int(30 * float(s2))
    if s1 == "PreTrain":
        if s2 == "Fin":
            p = 50
        else:
            p = 40 + 10 * int(10 * float(s2))
    if s1 == "Train":
        if s2 == "Fin":
            p = 100

        else:
            p = 50 + 50 * int(50 * float(s2))

    last_p = p
    if last_p == 100:
        last_p = 0
    print(latest_log, p)
    return p


def DownloadModel(model_name):
    model_path = ConfigReader.GetModelConfig(model_name)["model_out_path"]
    f = open(model_path, "rb")
    data = f.read()
    f.close()
    response = HttpResponse(data, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % "{}.pth".format(model_name)
    return response




def GetAttrById(data_name, attr_name, id):
    items = Base.QueryManyDocument(collection_name=data_name, filter={'id': id}, mask={"time": 1, attr_name: 1})
    if not items:
        return False

    ret = []
    for item in items:
        ret.append({'time': item['time'], 'value': item[attr_name]})

    return ret


import lightgbm as lgb
def PredictTimeSeries(data_name, attr_name, id):
    print(data_name, attr_name, id)
    raw = GetAttrById(data_name, attr_name, id)
    timeline = []
    train_valid = []
    train = []
    valid = []
    test = []

    l = 256
    f = 24

    for i, k in enumerate(raw):
        timeline.append(i)
        train_valid.append(k["value"])

    split_idx =  len(train_valid) #int(len(train_valid) * 0.99)
    train = train_valid[:split_idx]
    valid = train_valid[split_idx:]

    def make_train_data(ts, l):
        feature = []
        label = []
        for i in range(len(ts) - l):
            feature.append(ts[i:i+l])
            label.append(ts[i+l])

        return np.array(feature), np.array(label)

    feature, label = make_train_data(train, l)
    model = lgb.LGBMRegressor()
    model.fit(feature, label)


    def get_result(ts, n, model):
        result = []
        for i in range(n):
            temp = int(model.predict(np.array(ts).reshape(1, -1))[0])
            result.append(temp)
            ts = ts[1:] + [temp]
        return result

    #valid_pred = get_result(train[-l:], len(valid), model)
    test = get_result(train_valid[-l:], f, model)
    valid_pred = [None] * l + list(model.predict(feature).ravel()) + [None] * f

    #valid_pred = [None] * len(train) + valid_pred + [None] * len(test)
    test = [None] * len(train_valid) + test
    timeline = list(range(len(test)))

    return [timeline, train_valid+[None]*f, valid_pred, test]



from sklearn.ensemble import IsolationForest
from scipy import stats
def DetectionTimeSeries(data_name, attr_name, id):
    raw = GetAttrById(data_name, attr_name, id)
    timeline = []
    ts = []
    res = []

    for i, k in enumerate(raw):
        timeline.append(i)
        ts.append(k["value"])


    win_size = 24
    def minibatch(arr, batch_size):
        for i in range(0, len(arr), batch_size):
            yield arr[i:i + batch_size]

    train = list(minibatch(ts, win_size))[:-1]

    ratio = 0.1
    model = IsolationForest(max_samples=100, random_state=1024, contamination=ratio)
    model.fit(np.array(train))
    scores_pred = model.decision_function(np.array(train))
    threshold = stats.scoreatpercentile(scores_pred, 100 * ratio)
    pred = list(model.predict(np.array(train)))

    for i, row in enumerate(train):
        if pred[i] < threshold:
            res += row
        else:
            res += [None] * win_size
    res += [None] * (len(ts) - len(res))

    return [timeline, ts, res] 



if __name__ == "__main__":
    # Test Code
    pass
