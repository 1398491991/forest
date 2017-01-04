#coding=utf8
"""
爬虫的装饰器
"""
from forest.scheduler import scheduler
from functools import wraps
from forest.utils.async import is_request,is_response
from forest.utils.async import request_actions,response_actions
from forest.utils.exceptions import CallbackTypeException

def async(func):

    @wraps(func)
    def decorator(self,response_or_request,*args,**kwargs): # self == spider
        if is_request(response_or_request):
            # 回调类型是请求
            return request_actions(self,response_or_request)

        if is_response(response_or_request):
            # 回调类型是响应
            return response_actions(self,response_or_request)

        raise CallbackTypeException(u'回调类型必须是Response或者Request')
    return decorator


def checkout_request(request,self):
    """"""
    if not request.spider:
        request.spider=self
    return request

# def filter