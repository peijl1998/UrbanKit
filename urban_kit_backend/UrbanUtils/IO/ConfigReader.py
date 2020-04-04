#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Pei

import json
import os


def MakeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def GetModelConfigPath(name):
    p = "./Config/"
    MakeDir(p)
    return p + name + ".cfg"


def GetConfig():
    config_path = "../user_config.json"
    try:
        with open(config_path, "r") as f:
            content = f.read().strip()
            config_json = json.loads(content)
        return config_json
    except Exception as e:
        raise Exception("ConfigReader GetConfig Error: ", e)


def SetModelConfig(config, name):
    with open(GetModelConfigPath(name), "w") as f:
        f.write(json.dumps(config))


def GetModelConfig(model):
    if model == "SI-AGAN":
        config = {}
        with open(GetModelConfigPath(model), "r") as f:
            config["grid_size"] = 20
            config["generator_lr"] = 0.001
            config["discriminator_lr"] = 0.001
            config["pre_train_epoch"] = 2
            config["train_epoch"] = 10
            config["batch_size"] = 10
            config["mean_shift_radius"] = 25
            config["mean_shift_bandwith"] = 20
            temp_config = json.loads(f.read().strip())
            for k in ["grid_size", "generator_lr", "discriminator_lr", "pre_train_epoch", "train_epoch",
                      "batch_size", "mean_shift_radius", "mean_shift_bandwith"]:
                if k in temp_config.keys():
                    config[k] = temp_config[k]
            config["low_data_path"] = "../Temp/low_data.npy"
            config["high_data_path"] = "../Temp/high_data.npy"
            config["model_out_path"] = "../Temp/Generator.pth"
            config["log_path"] = "../Temp/log.txt"
            return config
    else:
        return {}


if __name__ == "__main__":
    pass
