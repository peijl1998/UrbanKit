from django.http import HttpResponse, JsonResponse
from UrbanHelper import Helper


def get_collection_list(request):
    return JsonResponse({"data": Helper.GetCollectionLists(), "msg": "success"})


def delete_collection(request):
    res = {"msg": "success"}
    if not Helper.DeleteCollection(request.GET.get("name")):
        res["msg"] = "failed"
    return JsonResponse(res)


def upload_csv_data(request):
    if request.method == "POST":
        fileDict = request.FILES.items()
        msg = "failed"
        if not fileDict:
            return JsonResponse({'msg': 'no file upload'})
        for k, v in fileDict:
            fileData = request.FILES.getlist(k)
            msg = "failed"
            for file in fileData:
                file_name = file._get_name()
                if len(file_name.split('.')) != 2 or file_name.split('.')[-1] != 'csv':
                    print("%s is not csv file!".format(file_name))
                file_str = ""
                if file.multiple_chunks():
                    for content in file.chunks():
                        file_str += str(content, 'utf-8')
                else:
                    file_str += str(file.read(), 'utf-8')
                if Helper.UploadCsv(file_name.split('.')[0], file_str):
                    msg = "success"
        return JsonResponse({'msg': msg})
    else:
        return JsonResponse({'msg': 'not post method'})


def get_time_line(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetTimeLine(data_name), 'msg': 'success'})


def get_attr_list(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetAttrList(data_name), 'msg': 'success'})

def get_id_list(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetIdList(data_name), 'msg': 'success'})

def get_id_position(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetIdPosition(data_name), 'msg': 'success'})

def get_attr_by_time(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    time_step = int(request.GET.get("time_step"))
    return JsonResponse({'data': Helper.GetAttrByTime(data_name, attr_name, time_step),
                         'msg': 'success'})

def get_top_attr_by_time(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    time_step = int(request.GET.get("time_step"))
    top = int(request.GET.get("top"))
    return JsonResponse({'data': Helper.GetTopAttrByTime(data_name, attr_name, time_step, top),
                         'msg': 'success'})

def get_id_stat_by_time(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    time_step = int(request.GET.get("time_step"))
    stat_name = request.GET.get("stat_name")
    return JsonResponse({'data': Helper.GetIdStatByTime(data_name, attr_name, time_step, stat_name),
                         'msg': 'success'})


def get_attr_by_id(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    id = request.GET.get("id")
    return JsonResponse({'data': Helper.GetAttrById(data_name, attr_name, id),
                         'msg': 'success'})


def get_multi_attr_by_id(request):
    data_name = request.GET.get("data_name")
    id = request.GET.get("id")
    attrs = request.GET.getlist("attr_names[]")
    return JsonResponse({'data': Helper.GetMultiAttrById(data_name, attrs, id),
                         'msg': 'success'})


def train_model(request):
    model_name = request.GET.get("model_name")
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    return JsonResponse({'data': True, 'msg': 'success'})


test_progress = 0
def get_train_progress(request):
    global test_progress
    model_name = request.GET.get("model_name")
    progress = 100
    progress = min(progress, test_progress)
    if progress == 100:
        test_progress = 0
    else:
        test_progress += 100
    return JsonResponse({'data': progress})


def test(request):
    return HttpResponse("OK")