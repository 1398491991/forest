#coding=utf8
"""
爬虫异步的装饰器
"""

from functools import wraps
from forest.utils.async import TaskRoute


def async(func):

    @wraps(func)
    def decorator(self,obj,*args,**kwargs): # self == spider
        tr=TaskRoute(func,self,obj)  # 路由分发
        tr.route()

    return decorator
