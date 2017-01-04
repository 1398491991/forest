#coding=utf8
"""
爬虫异步的装饰器
"""

from functools import wraps
from forest.utils.async import is_request,is_response
from forest.utils.async import request_actions,response_actions
from forest.utils.exceptions import CallbackTypeException

def async(func):

    @wraps(func)
    def decorator(self,response_or_request,*args,**kwargs): # self == spider
        if is_response(response_or_request):
            # 回调类型是响应
            return response_actions(func,self,response_or_request)

        if is_request(response_or_request): # 通过中间件过程可能有错误 返回 请求 重新尝试
            # 回调类型是请求
            return request_actions(func,self,response_or_request)

        raise CallbackTypeException(u'回调类型必须是Response或者Request')
    return decorator
