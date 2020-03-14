from django.contrib import admin
from django.urls import path
from UrbanKitInterface import views

urlpatterns = [
    path(r"test/", views.test),
    path(r'test_write/', views.test_write)
]
