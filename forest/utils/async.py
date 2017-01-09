#coding=utf-8
"""
针对装饰器 async 的一些工具
"""
from forest.http import RequestBase
from forest.http import ResponseBase
from forest.scheduler import tasks
from requests import Response # todo 暂时的
from forest.utils.item import ItemBase
from forest.utils.exceptions import AsyncResultNotIterException

def is_response(obj):
    return isinstance(obj,(ResponseBase,Response))

def is_request(obj):
    return isinstance(obj,RequestBase)


def is_item(obj):
    return isinstance(obj,ItemBase)


def request_actions(func,spider,request):
    """是请求对象 执行的动作"""
    if is_request(request): # 重试过程
        tasks.process_request.delay(request)#func(spider,request)

import warnings

def response_actions(func,spider,response):
    """是响应对象 执行的动作"""
    res=func(spider,response) # 返回处理后的下一步请求列表 爬虫的响应处理函数 xpath 等
    if not res:
        warnings.warn('async done')
        return
    try:
        for r in res:
            if not is_request(r): # 请求类型不是 请求 也是错误的
                warnings.warn('async type is not request')
                continue
            if not r.spider: # 没有设置类实例对象
                r.spider=spider
            tasks.process_request.delay(r)
    except TypeError:
        raise AsyncResultNotIterException(res)


def item_actions(func,spider,item):
    # 处理字段
    tasks.process_item.delay(item)