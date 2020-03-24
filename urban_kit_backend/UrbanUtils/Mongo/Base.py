#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

from UrbanUtils.Mongo import MongoConnect
from UrbanUtils.Mongo import Query
from bson import json_util

placeholder = {"_":-1}
mongo = MongoConnect.ConnectMongo()


def ReConnectMongo():
    global mongo
    mongo = MongoConnect.ConnectMongo()


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


def QueryDistinct(collection_name, key):
    if collection_name not in GetCollectionLists():
        return False
    return Query.QueryDistinct(collection = mongo[collection_name], key = key)

def QueryOneDocument(collection_name, filter=None, mask=None):
    if collection_name not in GetCollectionLists():
        return False
    return Query.QueryOneDocument(collection = mongo[collection_name], filter=filter, mask=mask)

def QueryManyDocument(collection_name, filter=None, mask=None):
    if collection_name not in GetCollectionLists():
        return False
    return json_util.dumps(Query.QueryManyDocument(collection = mongo[collection_name], filter=filter, mask=mask))



if __name__ == "__main__":
    # Test Code
    pass