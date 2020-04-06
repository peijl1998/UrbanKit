#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
# This file is to solve mongo I/O slow problem.
from bson import json_util

from UrbanUtils.Mongo import MongoConnect, Query
import pandas as pd
import numpy as np
import json
from bson import ObjectId
import datetime
import time

HAS_DATA = False
DATA = None
NAME = None
test_path = "D:\Files\Lab\kdd_beijing_17_18_all.csv"
placeholder = {"_":-1}
mongo = MongoConnect.ConnectMongo()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, o)

def GetCollectionLists():
    return mongo.list_collection_names()

def DeleteCollection(collection_name):
    if collection_name not in GetCollectionLists():
        return False
    else:
        try:
            mongo[collection_name].drop()
            return True
        except Exception as e:
            print("Delete Collection Failed:",e)
            return False

def CreateCollection(collection_name):
    if collection_name not in GetCollectionLists():
        mongo[collection_name].insert_one(placeholder)

def DeleteDocument(collection_name, filter):
    mongo[collection_name].delete_one(filter)

def CreateDocumentsInBatch(collection_name, docs):
    DeleteDocument(collection_name, placeholder)
    mongo[collection_name].insert_many(docs)



def UpdateMemData(collection_name, local_path=test_path):
    global DATA
    global NAME
    global HAS_DATA
    if not local_path:
        r = Query.QueryManyDocument(collection = mongo[collection_name])
        all_data = []

        last_time = time.time()
        idx = 0
        while True:
            i = r.next()
            idx += 1
            if idx % 1 == 0:
                print ("avg time for one: ", (time.time() - last_time))
                last_time = time.time()
            #all_data.append(i)
        data_dict = {}
        for item in all_data:
            for k in item.keys():
                if k in data_dict:
                    data_dict[k].append(item[k])
                else:
                    data_dict[k] = [item[k]]
        DATA = pd.DataFrame.from_dict(data_dict)
        NAME = collection_name
        HAS_DATA = True
    else:
        DATA = pd.read_csv(local_path)
        NAME = collection_name
        HAS_DATA = True

def QueryDistinct(collection_name, key):
    global DATA
    global NAME
    global HAS_DATA
    if not HAS_DATA or NAME != collection_name:
        UpdateMemData(collection_name)
    return np.unique(DATA[key].values).tolist()


# TODO(Pei): Here only supports one key filter now. Improve it later.
def QueryOneDocument(collection_name, filter=None, mask=None):
    global DATA
    global NAME
    global HAS_DATA
    if not HAS_DATA or NAME != collection_name:
        UpdateMemData(collection_name)
    cols = []
    if not mask:
        cols = DATA.columns
    else:
        for c in DATA.columns:
            if c in mask and mask[c] != 0:
                cols.append(c)

    if not filter:
        ret = {}
        for k in cols:
            ret[k] = DATA[k][0]
        return ret
    else:
        f_key = list(filter.keys())[0]
        f_value = filter[f_key]

        ret = {}
        T_DATA = DATA[DATA[f_key] == f_value][cols].copy(deep=True)
        for k in cols:
            ret[k] = T_DATA[k].values[0]
        del T_DATA

        return ret

# TODO(Pei): Here only supports one key filter now. Improve it later.
def QueryManyDocument(collection_name, filter=None, mask=None):
    global DATA
    global NAME
    global HAS_DATA
    if not HAS_DATA or NAME != collection_name:
        UpdateMemData(collection_name)
    cols = []
    if not mask:
        cols = DATA.columns
    else:
        for c in DATA.columns:
            if c in mask and mask[c] != 0:
                cols.append(c)

    if not filter:
        ret = []
        for i in range(DATA.shape[0]):
            temp = {}
            for k in cols:
                temp[k] = DATA[k][i]
            ret.append(temp)
        return ret
    else:
        f_key = list(filter.keys())[0]
        f_value = filter[f_key]
        ret = []
        T_DATA = DATA[DATA[f_key] == f_value][cols].copy(deep=True)
        for i in range(T_DATA.shape[0]):
            temp = {}
            for k in cols:
                temp[k] = T_DATA[k].values[i]
            ret.append(temp)
        del T_DATA
        return ret

if __name__ == "__main__":
    print (QueryDistinct("kdd_beijing_17_18_all.csv", "time"))