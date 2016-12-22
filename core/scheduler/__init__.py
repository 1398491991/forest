#coding=utf-8
#调度器
from celery_crawl.import_api import Request

def callback_request(request,**kwargs):
    # assert isinstance(request,dict)
    request=Request(**request)
    response=request.curl()
    return request
