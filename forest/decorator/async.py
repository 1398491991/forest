#coding=utf8
"""
爬虫的装饰器
"""
from forest.core.scheduler import process_request
from functools import wraps

def async_request(func):
    """
    爬虫异步回调请求的装饰器
    """
    @wraps(func)
    def decorator(request_or_response):
        # try:
            rq_list=func(request_or_response)
        # except:
        #     pass
        # else:
            for rq in rq_list:
                process_request.delay(rq.to_dict())
    return decorator