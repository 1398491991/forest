#coding=utf8
"""
爬虫异步的装饰器
"""

from functools import wraps
from forest.utils.async import is_request,is_response,is_item
from forest.utils.async import request_actions,response_actions,item_actions
from forest.utils.exceptions import CallbackTypeException

def async(func):

    @wraps(func)
    def decorator(self,obj,*args,**kwargs): # self == spider
        if is_response(obj):
            # 回调类型是响应
            return response_actions(func,self,obj)

        if is_request(obj): # 通过中间件过程可能有错误 返回 请求 重新尝试
            # 回调类型是请求
            return request_actions(func,self,obj)
        # 接下来是 item 等等 存入数据库
        if is_item(obj):
            return item_actions(func,self,obj)
        # 否则就报错
        raise CallbackTypeException()
    return decorator
