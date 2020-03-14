#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei


from . import models


def Write(collection_name, doc):
	try:
		if collection_name == 'test':
			models.test.objects.create(**doc)
		else:
			raise Exception("collection_name not found!")
	except Exception as e:
		raise Exception("Data Write Error: ", e)



if __name__ == '__main__':
	pass