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
    def decorator(self,a):#*args,**kwargs):
        # print type(request_or_response)
        # print args
        # print kwargs
        print a
        request_or_response=a
        # self,request_or_response=args
        if isinstance(request_or_response,RequestBase):
            # todo  重新请求 待明确
            d=request_or_response.to_dict()
            return d
        elif isinstance(request_or_response,ResponseBase)\
                or not request_or_response: # response
            rq_list=func(request_or_response)
            for rq in rq_list:
                process_request.delay(rq.to_dict())
        else:
            raise HttpTypeException

    return decorator