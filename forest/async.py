#coding=utf-8


from functools import wraps
from worker.scheduler import EnqueueScheduler
from http.response import Response
from http.request import Request
from worker.scheduler import enqueue_scheduler

def async(func):

    @wraps(func)
    def decorator(self,obj): # self == spider
        if isinstance(obj,Response):
            res=func(self,obj)
            if not isinstance(res,(list,tuple)):
                res=[res]
        else:
            # method=obj['method'].upper()
            res=[Request(**obj)]
        return map(enqueue_scheduler.scheduler,res)

    return decorator