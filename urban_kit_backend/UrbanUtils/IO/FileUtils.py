#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

def WriteFile(s, path, mode="a"):
    with open(path, mode) as f:
        f.write(s)