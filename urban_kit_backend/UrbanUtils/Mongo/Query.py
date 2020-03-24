#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

def QueryDistinct(collection, key):
    return collection.distinct(key)

def QueryOneDocument(collection, filter=None, mask=None):
    if mask is None:
        mask = {}
    if filter is None:
        filter = {}
    mask["_id"] = 0
    return collection.find_one(filter, mask)

def QueryManyDocument(collection, filter=None, mask=None):
    if mask is None:
        mask = {}
    if filter is None:
        filter = {}
    mask["_id"] = 0
    return collection.find(filter, mask)