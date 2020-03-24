#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

from UrbanUtils.IO import ConfigReader
import logging
import pymongo

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='util.log',filemode='a')
logger = logging.getLogger(__name__)

def ConnectMongo():
    config = ConfigReader.GetConfig()
    try:
        database = config["mongodb"]
        collection = database["database"]
        ip = database["address"]
        user = database["user"]
        pwd = database["password"]
        port = database["port"]
        host = 'mongodb://{}:{}@{}:{}/?authSource={}&authMechanism=SCRAM-SHA-1'.format(user, pwd, ip, port, collection)
        mongo = pymongo.MongoClient(host)[collection]
        print ("MongoDB Connect Successful!")
        return mongo
    except Exception as e:
        raise Exception("Setup Database Error: ", e)


if __name__ == "__main__":
    # Test Code
    pass