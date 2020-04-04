from django.urls import path
from . import views

urlpatterns = [
    path(r"data/get_collection_list", views.get_collection_list),
    path(r"data/delete_collection", views.delete_collection),
    path(r"data/upload_csv_data", views.upload_csv_data),

    path(r'query/get_time_line', views.get_time_line),
    path(r'query/get_attr_list', views.get_attr_list),
    path(r'query/get_id_list', views.get_id_list),
    path(r'query/get_id_position', views.get_id_position),
    path(r'query/get_attr_by_time', views.get_attr_by_time),
    path(r'query/get_top_attr_by_time', views.get_top_attr_by_time),
    path(r'query/get_id_stat_by_time', views.get_id_stat_by_time),
    path(r'query/get_attr_by_id', views.get_attr_by_id),
    path(r'query/get_multi_attr_by_id', views.get_multi_attr_by_id),

    path(r'model/train_model', views.train_model),
    path(r'model/get_train_progress', views.get_train_progress),
    path(r'model/set_model_params', views.set_model_params),

    path(r'test/', views.test)
]
