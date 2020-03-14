from django.db import models
import mongoengine

class test(mongoengine.Document):
	col1 = mongoengine.StringField(max_length = 16)
	col2 = mongoengine.IntField(default = 0)
	