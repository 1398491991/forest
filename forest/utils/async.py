#coding=utf-8
"""
针对装饰器 async 的一些工具
"""
from forest.http import RequestBase
from forest.http import ResponseBase
from forest.scheduler import scheduler
from requests import Response # 暂时的

def is_response(obj):
    return isinstance(obj,(ResponseBase,Response))

def is_request(obj):
    return isinstance(obj,RequestBase)

def request_actions(func,spider,request):
    """是请求对象 执行的动作"""
    scheduler.process_request.delay(request)#func(spider,request)


def response_actions(func,spider,response):
    """是响应对象 执行的动作"""
    res=func(spider,response) # 返回请求列表
    if not res:
        return
    for r in res:
        if not r.spider: # 没有类实例对象
            r.spider=spider
        scheduler.process_request.delay(r)