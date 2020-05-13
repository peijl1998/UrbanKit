import os

from django.http import HttpResponse, JsonResponse
from UrbanHelper import Helper
from UrbanUtils.IO import ConfigReader
from UrbanHelper.Helper import MyEncoder


def get_collection_list(request):
    return JsonResponse({"data": Helper.GetCollectionLists(), "msg": "success"}, encoder=MyEncoder)


def delete_collection(request):
    res = {"msg": "success"}
    if not Helper.DeleteCollection(request.GET.get("name")):
        res["msg"] = "failed"
    return JsonResponse(res, encoder=MyEncoder)

def upload_model(request):
    print(request.FILES.keys())
    file = request.FILES.get("file", None)
    if not file:
        return JsonResponse({"data": "no file for upload.", "msg": "failed"})
    else:
        model_name = file.name.split(".")[0]
        path = ConfigReader.GetModelConfig(model_name)["model_out_path"]
        if os.path.exists(path):
            os.remove(path)
        dst = open(path, "wb+")
        for chunk in file.chunks():
            dst.write(chunk)
        dst.close()
        return JsonResponse({"data": "OK", "msg": "success"})

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
        return JsonResponse({'msg': 'not post method'}, encoder=MyEncoder)


def get_time_line(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetTimeLine(data_name), 'msg': 'success'}, encoder=MyEncoder)


def get_attr_list(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetAttrList(data_name), 'msg': 'success'}, encoder=MyEncoder)


def get_id_list(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetIdList(data_name), 'msg': 'success'}, encoder=MyEncoder)


def get_id_position(request):
    data_name = request.GET.get("data_name")
    return JsonResponse({'data': Helper.GetIdPosition(data_name), 'msg': 'success'}, encoder=MyEncoder)


def get_attr_by_time(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    time_step = int(request.GET.get("time_step"))
    return JsonResponse({'data': Helper.GetAttrByTime(data_name, attr_name, time_step),
                         'msg': 'success'}, encoder=MyEncoder)


def get_top_attr_by_time(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    time_step = int(request.GET.get("time_step"))
    top = int(request.GET.get("top"))
    return JsonResponse({'data': Helper.GetTopAttrByTime(data_name, attr_name, time_step, top),
                         'msg': 'success'}, encoder=MyEncoder)


def get_id_stat_by_time(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    time_step = int(request.GET.get("time_step"))
    stat_name = request.GET.get("stat_name")
    return JsonResponse({'data': Helper.GetIdStatByTime(data_name, attr_name, time_step, stat_name),
                         'msg': 'success'}, encoder=MyEncoder)


def get_attr_by_id(request):
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    id = request.GET.get("id")
    return JsonResponse({'data': Helper.GetAttrById(data_name, attr_name, id),
                         'msg': 'success'}, encoder=MyEncoder)


def get_multi_attr_by_id(request):
    data_name = request.GET.get("data_name")
    id = request.GET.get("id")
    attrs = request.GET.getlist("attr_names[]")
    return JsonResponse({'data': Helper.GetMultiAttrById(data_name, attrs, id),
                         'msg': 'success'}, encoder=MyEncoder)

def predict_time_series(request):
    data_name = request.GET.get("data_name")
    id = request.GET.get("id")
    attrs = request.GET.get("attr_name")

    return JsonResponse({'data': Helper.PredictTimeSeries(data_name, attrs, id),
                         'msg': 'success'}, encoder=MyEncoder)


def detection_time_series(request):
    data_name = request.GET.get("data_name")
    id = request.GET.get("id")
    attrs = request.GET.get("attr_name")

    return JsonResponse({'data': Helper.DetectionTimeSeries(data_name, attrs, id),
                         'msg': 'success'}, encoder=MyEncoder)

def cal_corr(request):
    method = request.GET.get("method")
    data_name = request.GET.get("data_name")
    id = request.GET.get("id")
    attrs = request.GET.getlist("attr_names[]")

    return JsonResponse({'data': Helper.CalCorr(data_name, attrs, id, method),
                         'msg': 'success'}, encoder=MyEncoder)

def train_model(request):
    model_name = request.GET.get("model_name")
    data_name = request.GET.get("data_name")
    attr_name = request.GET.get("attr_name")
    return JsonResponse({'data': Helper.TrainModel(model_name, data_name, attr_name), 'msg': 'success'},
                        encoder=MyEncoder)


def get_train_progress(request):
    model_name = request.GET.get("model_name")
    return JsonResponse({'data': Helper.GetTrainProgress(model_name)}, encoder=MyEncoder)


def predict_one(request):
    model_name = request.GET.get("model_name")
    long = request.GET.get("longitude")
    lat = request.GET.get("latitude")
    data_name = request.GET.get("data_name")
    time_step = int(request.GET.get("time_step"))
    attr_name = request.GET.get("attr_name")
    return JsonResponse({'data': Helper.PredictOne(model_name, data_name, long, lat, time_step, attr_name),
                         'msg': 'success'}, encoder=MyEncoder)


def predict_many(request):
    model_name = request.GET.get("model_name")
    data_name = request.GET.get("data_name")
    time_step = int(request.GET.get("time_step"))
    attr_name = request.GET.get("attr_name")
    return JsonResponse({'data': Helper.PredictMany(model_name, data_name, time_step, attr_name),
                         'msg': 'success'}, encoder=MyEncoder)


def set_model_params(request):
    model_name = request.GET.get("model_name")
    if model_name == "SI-AGAN":
        config = {}
        for k in ["grid_size", "generator_lr", "discriminator_lr", "pre_train_epoch", "train_epoch",
                  "batch_size", "mean_shift_radius", "mean_shift_bandwith"]:
            if k in request.GET.keys():
                config[k] = request.GET.get(k)
        ConfigReader.SetModelConfig(config, "SI-AGAN")

    return JsonResponse({"msg": "success"}, encoder=MyEncoder)


def remove_log(request):
    return JsonResponse({'msg': Helper.RemoveLog(request.GET.get("model_name"))}, encoder=MyEncoder)

def download_model(request):
    return Helper.DownloadModel(request.GET.get("model_name"))



def test(request):
    return HttpResponse("OK")
