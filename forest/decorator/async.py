#coding=utf8
"""
爬虫的装饰器
"""
from forest.scheduler import scheduler
from functools import wraps
from forest.http import RequestBase
from forest.http import ResponseBase
from forest.utils.exceptions import HttpTypeException

def async(func):

    @wraps(func)
    def decorator(self,*args,**kwargs):
        print self,args,kwargs,'###############'
        res=func(self,*args,**kwargs)
        for r in res:
            if not r.spider:
                r.spider=self
            scheduler.process_request.delay(r)
    return decorator



# def async_request(func):
#     """
#     爬虫异步回调请求的装饰器
#     """
#     @wraps(func)
#     def decorator(self):#*args,**kwargs):
#         # self,request_or_response=args
#             print self
#             rq_list=func(self)
#             for rq in rq_list:
#                 if not rq.spider:
#                     rq.spider=self
#                 process_request.delay(rq)
#     return decorator