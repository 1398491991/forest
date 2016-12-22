#coding=utf-8
#调度器
from celery_crawl.import_api import Request
from celery_crawl.middleware.manager import ManagerMiddleware
def callback_request(request,**kwargs):
    # assert isinstance(request,dict)
    request=Request(**request)
    # todo do something...
    return ManagerMiddleware.process(request)
