#coding=utf8
"""
爬虫的装饰器
"""
from forest.core.scheduler import process_request
from functools import wraps

def delay(func):
    """爬虫回调请求的装饰器"""
    @wraps(func)
    def decorator(*args,**kwargs):
        # try:
            rq_list=func(*args,**kwargs)
        # except:
        #     pass
        # else:
            for rq in rq_list:
                process_request.delay(rq)
    return decorator