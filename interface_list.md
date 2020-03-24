前后端联调才算完成。

1. - [x] /data/get_collection_list
      - 获取已有数据列表
      - return  Array
      - GET
2. - [x] /data/delete_collection?name=xxx
      - 删除某个数据
      - return bool
      - GET
3. - [x] /data/upload_csv_data
      - 上传数据
      - POST
4. - [x] /query/get_time_line?data_name=xxx
      - 获取xxx collection中时间元信息    【需要对时间排序】
      - return Array
      - GET
5. - [x] /query/get_attr_list?data_name=xxx
      - 获取xxx collection中attr列表
      - return  Array
      - GET
6. - [x] /query/get_id_list?data_name=xxx
      - 获取xxx collection中id列表
      - return Array
      - GET
7. - [x] /query/get_id_position?data_name=xxx
      - 获取xxx collection中id及经纬度 Dict
      - return Dict
      - GET
8. - [x] /query/get_attr_by_time?data_name=xxx&time_step=xxx&attr_name=xxx
      - 获取xxx collection中id的attr的值，根据时间。
      - return Dict
      - GET
9. - [x] /query/get_top_attr_by_time?data_name=xxx&time_step=xxx&attr_name=xxx&top=xxx
      - 获取xxx collection中id的top attr值
      - return Dict
      - GET
10. - [x] /query/get_id_stat_by_time?data_name=xxx&time_step=xxx&attr_name=xxx&stat_name=xxx
      - 获取某时间某属性的统计量
      - return float
      - GET
11. - [x] /query/get_attr_by_id?data_name=xxx&attr_name=xxx&id=xxx
      - 获取某id某属性所有时间的值
      - return Dict
      - GET
12. - [x] /query/get_mult_attr_by_id?data_name=xxx&attr_names=xxx&id=xxx
      - 获取某id多属性所有时间的值
      - return Dict   [{'time':xxx,  'value': {'attr1':x, 'attr2':x}},...]
      - GET