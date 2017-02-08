#coding=utf-8
from request import Request
from ..utils.serializable import load_json,load_pickle
from forest.async import async

class AddRequest(object):
    def __init__(self,request):
        self.request= request

    @classmethod
    def from_json(cls,request_json):
        return cls(Request(**load_json(request_json)))


    @classmethod
    def from_dict(cls,request_dict):
        return cls(Request(**request_dict))

    @classmethod
    def from_pickle(cls,request_pickle):
        return cls(Request(**load_pickle(request_pickle)))

    def add(self):
        return async.apply_async(self.request)


