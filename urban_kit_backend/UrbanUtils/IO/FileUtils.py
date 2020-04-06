#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei
import os

error_file = "./Error.txt"

def WriteFile(s, path, mode="a"):
    with open(path, mode) as f:
        f.write(s)


def DeleteFile(path):
    try:
        os.remove(path)
    except Exception as e:
        WriteFile("Delete File Error: "+str(e), error_file, "a")

def ReadFile(path):
    if not os.path.exists(path):
        return False
    with open(path, "r") as f:
        return f.readlines()