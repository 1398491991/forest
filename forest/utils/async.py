#coding=utf-8
"""
针对装饰器 async 的一些工具
"""
from forest.http import RequestBase
from forest.http import ResponseBase
from forest.scheduler import scheduler

# res=func(self,response_or_request,*args,**kwargs)
# for r in res:
#     r=checkout_request(r,self)
#     scheduler.process_request.delay(r)

def is_response(obj):
    return isinstance(obj,ResponseBase)

def is_request(obj):
    return isinstance(obj,RequestBase)

def request_actions(spider,request):
    """是请求对象 执行的动作"""
    pass


def response_actions(spider,response):
    """是响应对象 执行的动作"""
    pass