#coding=utf8
"""
爬虫异步的装饰器
"""

from functools import wraps
from forest.utils.async import TaskRoute,RestoreRequest


def async(func):

    @wraps(func)
    def decorator(self,obj,*args,**kwargs): # self == spider
        rr=RestoreRequest(func,self,obj)
        rr.restore() # 恢复请求
        tr=TaskRoute(func,self,obj)  # 路由分发
        tr.route()

    return decorator
