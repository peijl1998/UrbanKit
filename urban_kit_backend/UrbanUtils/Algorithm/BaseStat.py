#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

import numpy as np


def ToArray(arr):
    return arr if type(arr) != type([]) else np.array(arr)


def Mean(arr):
    return np.mean(arr)


def Max(arr):
    return np.max(arr)


def Min(arr):
    return np.min(arr)


def Median(arr):
    return np.median(arr)


def Variance(arr):
    return np.var(arr)


def Q1(arr):
    return np.percentile(arr, 0.25)


def Q3(arr):
    return np.percentile(arr, 0.75)
