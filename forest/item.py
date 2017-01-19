#coding=utf-8
from utils.serializable import dump_json

class SimpleItem(dict):
    def to_json(self):
        return dump_json(self)
