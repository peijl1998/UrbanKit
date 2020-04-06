import axios from 'axios'
import global_ from '@/api/global_variable.js'
import config_ from '@/api/global_config.js'

function GetApi(api_name) {
  return "http://" + config_.backend + api_name;
}


async function GetDataList() {
  var api = GetApi(global_.apis["get_data_list"]);
  const res = await axios.get(api);
  return res.data;
}

async function DeleteData(name) {
  var api = GetApi(global_.apis["delete_data"]);
  const res = await axios.get(api, {
    params: {
      name: name
    }
  });
  return res.data;
}

async function GetTimeLine(name) {
  var api = GetApi(global_.apis["get_time_line"]);
  const res = await axios.get(api, {
    params: {
      data_name: name
    }
  });
  return res.data;
}

async function GetAttrList(name) {
  var api = GetApi(global_.apis["get_attr_list"]);
  const res = await axios.get(api, {
    params: {
      data_name: name
    }
  });
  return res.data;
}

async function GetIdList(name) {
  var api = GetApi(global_.apis["get_id_list"]);
  const res = await axios.get(api, {
    params: {
      data_name: name
    }
  });
  return res.data;
}

async function GetIdPosition(name) {
  var api = GetApi(global_.apis["get_id_position"]);
  const res = await axios.get(api, {
    params: {
      data_name: name
    }
  });
  return res.data;
}

async function GetAttrByTime(data_name, attr_name, time_step) {
  var api = GetApi(global_.apis["get_attr_by_time"]);
  const res = await axios.get(api, {
    params: {
      data_name: data_name,
      attr_name: attr_name,
      time_step: time_step,
    }
  });
  return res.data;
}

async function GetTopAttrByTime(data_name, attr_name, time_step, top) {
  var api = GetApi(global_.apis["get_top_attr_by_time"]);
  const res = await axios.get(api, {
    params: {
      data_name: data_name,
      attr_name: attr_name,
      time_step: time_step,
      top: top
    }
  });
  return res.data;
}

async function GetIdStatByTime(data_name, attr_name, time_step, stat_name) {
  var api = GetApi(global_.apis["get_id_stat_by_time"]);
  const res = await axios.get(api, {
    params: {
      data_name: data_name,
      attr_name: attr_name,
      time_step: time_step,
      stat_name: stat_name
    }
  });
  return res.data;
}

async function GetAttrById(data_name, attr_name, id) {
  var api = GetApi(global_.apis["get_attr_by_id"]);
  const res = await axios.get(api, {
    params: {
      data_name: data_name,
      attr_name: attr_name,
      id: id
    }
  });
  return res.data;
}

async function GetMultiAttrById(data_name, attr_names, id) {
  var api = GetApi(global_.apis["get_multi_attr_by_id"]);
  const res = await axios.get(api, {
    params: {
      data_name: data_name,
      attr_names: attr_names,
      id: id
    }
  });
  return res.data;
}

async function SetModelParameter(model_name, params) {
  var api = GetApi(global_.apis["set_model_parameter"]);
  const res = await axios.get(api, {
    params: {
      model_name: model_name,
      grid_size: params["grid_size"],
      generator_lr: params["generator_lr"],
      discriminator_lr: params["discriminator_lr"],
      pre_train_epoch: params["pre_train_epoch"],
      train_epoch: params["train_epoch"],
      batch_size: params["batch_size"],
      mean_shift_radius: params["ms_radius"],
      mean_shift_bandwith: params["ms_bandwith"],
    }
  });
  return res.data;
}

async function TrainModel(model_name, data_name, attr_name) {
  var api = GetApi(global_.apis["train_model"]);
  const res = await axios.get(api, {
    params: {
      model_name: model_name,
      data_name: data_name,
      attr_name: attr_name,
    }
  });
  return res.data;
}

async function GetTrainProgress(model_name) {
  var api = GetApi(global_.apis["get_train_progress"]);
  const res = await axios.get(api, {
    params: {
      model_name: model_name
    }
  });
  return res.data;
}

async function PredictOne(long, lat, model_name, data_name, time_step, attr_name) {
  var api = GetApi(global_.apis["predict_one"]);
  const res = await axios.get(api, {
    params: {
      longitude: long,
      latitude: lat,
      data_name: data_name,
      model_name: model_name,
      time_step: time_step,
      attr_name: attr_name
    }
  });
  return res.data;
}

async function PredictMany(model_name, data_name, time_step, attr_name) {
  var api = GetApi(global_.apis["predict_many"]);
  const res = await axios.get(api, {
    params: {
      model_name: model_name,
      data_name: data_name,
      time_step: time_step,
      attr_name: attr_name
    }
  });
  return res.data;
}

async function RemoveLog(model_name) {
  var api = GetApi(global_.apis["remove_log"])
  const res = await axios.get(api, {
    params: {
      model_name: model_name
    }
  });
  return res.data;
}

async function DownloadModel(model_name) {
  var api = GetApi(global_.apis["download_model"]);
  window.open(api+"?"+"model_name="+model_name);
}



function sleep(ms) {
  var start = new Date().getTime();
  while (true) {
    var time = new Date().getTime();
    if (time - start > ms) {
      break;
    }
  }
}

export default {
  install: function(Vue) {
    Vue.prototype.GetDataList = () => GetDataList(),
      Vue.prototype.DeleteData = (name) => DeleteData(name),
      Vue.prototype.GetTimeLine = (name) => GetTimeLine(name),
      Vue.prototype.GetAttrList = (name) => GetAttrList(name),
      Vue.prototype.GetIdList = (name) => GetIdList(name),
      Vue.prototype.GetIdPosition = (name) => GetIdPosition(name),
      Vue.prototype.GetAttrByTime = (data_name, attr_name, time_step) => GetAttrByTime(data_name, attr_name, time_step),
      Vue.prototype.GetAttrById = (data_name, attr_name, id) => GetAttrById(data_name, attr_name, id),
      Vue.prototype.GetMultiAttrById = (data_name, attr_names, id) => GetMultiAttrById(data_name, attr_names, id),
      Vue.prototype.GetTopAttrByTime = (data_name, attr_name, time_step, top) => GetTopAttrByTime(data_name, attr_name, time_step, top),
      Vue.prototype.GetIdStatByTime = (data_name, attr_name, time_step, stat_name) => GetIdStatByTime(data_name, attr_name, time_step, stat_name),
      Vue.prototype.sleep = (ms) => sleep(ms),
      Vue.prototype.SetModelParameter = (model_name, params) => SetModelParameter(model_name, params),
      Vue.prototype.RemoveLog = (model_name) => RemoveLog(model_name),
      Vue.prototype.DownloadModel = (model_name) => DownloadModel(model_name),
      Vue.prototype.TrainModel = (model_name, data_name, attr_names) => TrainModel(model_name, data_name, attr_names),
      Vue.prototype.GetTrainProgress = (model_name) => GetTrainProgress(model_name),
      Vue.prototype.PredictOne = (long, lat, model_name, data_name, time_step, attr_name) => PredictOne(long, lat, model_name, data_name, time_step, attr_name),
      Vue.prototype.PredictMany = (model_name, data_name, time_step, attr_name) => PredictMany(model_name, data_name, time_step, attr_name)
  }
}
