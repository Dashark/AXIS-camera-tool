# -*- coding:utf-8 -*-
import json
import os
from app_path import base_dir
config_file = os.path.join(base_dir,r"conf/config.json")

class Config:
    def __init__(self):
        with open(config_file, "r",encoding="UTF-8") as f:
            config = json.loads(f.read())
        for key, value in config.items():
            setattr(self, key, value)

    def __getattr__(self, item):
        return None

    def get(self, item):
        return getattr(self, item)

    def set(self, item, value):
        setattr(self, item, value)

    def save(self):
        with open(config_file, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.__dict__, indent=4))


