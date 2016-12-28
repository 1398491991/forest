#coding=utf8
"""
爬虫的装饰器
"""
from forest.core.scheduler import process_request
from functools import wraps
from forest.http import RequestBase
from forest.http import ResponseBase

def async_request(func):
    """
    爬虫异步回调请求的装饰器
    """
    @wraps(func)
    def decorator(request_or_response):
        if isinstance(request_or_response,RequestBase):
            # todo  重新请求
            pass
        else: # response
            rq_list=func(request_or_response)
            for rq in rq_list:
                process_request.delay(rq.to_dict())
    return decorator