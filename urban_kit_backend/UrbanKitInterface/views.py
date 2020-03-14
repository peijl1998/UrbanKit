from django.http import HttpResponse
from DataHandler import handler

def test(request):
	return HttpResponse("Hello world!")

def test_write(request):
	handler.Write("test", {"col1": "test", "col2": 0})
	return HttpResponse("OK")