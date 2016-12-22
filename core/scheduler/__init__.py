#coding=utf-8
#调度器
from forest.import_api import Request
from forest.import_api import ManagerMiddleware

def process_request(request,**kwargs):
    # assert isinstance(request,dict)
    request=Request(**request)
    # todo do something...
    return ManagerMiddleware.process(request)
