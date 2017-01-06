#coding=utf-8
"""
针对装饰器 async 的一些工具
"""
from forest.http import RequestBase
from forest.http import ResponseBase
from forest.scheduler import scheduler
from requests import Response # todo 暂时的
from forest.utils.item import ItemBase

def is_response(obj):
    return isinstance(obj,(ResponseBase,Response))

def is_request(obj):
    return isinstance(obj,RequestBase)


def is_item(obj):
    return isinstance(obj,ItemBase)


def request_actions(func,spider,request):
    """是请求对象 执行的动作"""
    scheduler.process_request.delay(request)#func(spider,request)


def response_actions(func,spider,response):
    """是响应对象 执行的动作"""
    res=func(spider,response) # 返回处理后的下一步请求列表 爬虫的响应处理函数 xpath 等
    if not res:
        return
    for r in res:
        if not r.spider: # 没有设置类实例对象
            r.spider=spider
        scheduler.process_request.delay(r)


def item_actions(func,spider,item):
    # 处理字段
    scheduler.process_item.delay(item) # 异步处理item