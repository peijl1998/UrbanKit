#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

import json
import os


# Basic Settings
config_path = "../user_config.json"


def GetConfig():
	try:
		config_json = {}
		with open(config_path, "r") as f:
			content = f.read().strip()
			config_json = json.loads(content)
		return config_json
	except Exception as e:
		raise Exception("ConfigReader GetConfig Error: ", e)


if __name__ == "__main__":
	# Test Code
	pass