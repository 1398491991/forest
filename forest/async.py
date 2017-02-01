#coding=utf-8
from functools import wraps
from http.request import Request
from http.response import Response
from .item import Item
from worker.scheduler import enqueueRequestScheduler
from worker.scheduler import enqueueItemScheduler

def async(func):

    @wraps(func)
    def decorator(self,obj): # self == spider
        if not obj or isinstance(obj,Item):
            return

        res=[]
        if isinstance(obj,Response):
            res=func(self,obj) # 执行解析方法
            if not isinstance(res,(list,tuple)):
                res=[res]

        elif isinstance(obj,Request):# 无用的请求 再次
            res=[obj]

        for obj in res: # 针对结果 异步处理
            if isinstance(obj,(Request,Item)):
                if not obj.from_spider:
                    obj.from_spider=self.name
                if isinstance(obj,Request):
                    enqueueRequestScheduler.enqueue(obj)
                elif isinstance(obj,Item):
                    enqueueItemScheduler.enqueue(obj)


    return decorator