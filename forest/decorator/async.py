#coding=utf8
"""
爬虫的装饰器
"""
from forest.core.scheduler import process_request
from functools import wraps
from forest.http import RequestBase
from forest.http import ResponseBase
from forest.utils.exceptions import HttpTypeException

def async_request(func):
    """
    爬虫异步回调请求的装饰器
    """
    @wraps(func)
    def decorator(self):#*args,**kwargs):
        # self,request_or_response=args
            print self
            rq_list=func(self)
            for rq in rq_list:
                if not rq.spider:
                    rq.spider=self
                process_request.delay(rq)
    return decorator