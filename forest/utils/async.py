#coding=utf-8
"""
针对装饰器 async 的一些工具
"""
from forest.http import RequestBase
from forest.http import ResponseBase
from forest.scheduler import tasks
from forest.utils.item import ItemBase
import warnings
from collections import Iterable
from forest.utils.spider import get_spider_collect_status,get_spider_status
from forest.utils.request import request_collect_to_redis,request_restore_from_redis


def is_iter(obj):
    """可迭代的"""
    return isinstance(obj,Iterable)

def is_response(obj):
    return isinstance(obj,(ResponseBase))

def is_request(obj):
    return isinstance(obj,RequestBase)


def is_item(obj):
    return isinstance(obj,ItemBase)

class TaskRoute(object):
    def __init__(self,func,spider,obj):
        self.func=func
        self.spider=spider
        self.obj=obj

    def delay_request(self,request):

        def if_not_spider(request):
            """没有spider object"""
            if not request.spider:
                request.spider=self.spider
            return request

        request=if_not_spider(request)
        tasks.process_request.delay(request)



    def delay_item(self,item):
        tasks.process_item.delay(item)

    def _route(self,obj):
        if is_request(obj):
            return self.delay_request(obj)
        if is_item(obj):
            return self.delay_item(obj)
        warnings.warn('route object type unknown %s , ignore'%obj)

    def _make_route(self,res):
        """创建分发任务"""
        if res:
            if not is_iter(res):
                res=[res]
            for obj in res:
                self._route(obj)

        else:
            warnings.warn('route content is Null')

    def route(self):
        if is_response(self.obj): # 是响应
            callback_result=self.func(self.spider,self.obj) # 回调
        else:
            callback_result=self.obj

        return self._make_route(callback_result)



class CollectRequest(object):
    def __init__(self,func,spider,obj):
        self.func=func
        self.spider=spider
        self.obj=obj

    def collect(self):
        # 返回的 bool 是否进行下一步分发工序
        name=self.spider.name
        if get_spider_status(name)=='off' and is_request(self.obj):
            if get_spider_collect_status(name):
                request_collect_to_redis(name,request=self.obj)
            return False
        # 爬虫关闭 检测是否同步请求
        # 如果是请求就收集到redis
        return True


class RestoreRequest(object):
    """还原请求"""

    def __init__(self,func,spider,obj):
        self.func=func
        self.spider=spider
        self.obj=obj

    def restore(self):
        """恢复请求对象 始终返回 True 并且会分发出去"""
        rs=request_restore_from_redis(self.spider.name)
        for r in rs:
            rp=self._parse(r)
            tr=TaskRoute(*rp)
            tr.route() # 分发
        return True


    def _parse(self,request):
        return (getattr(request.spider,request.callback),
                request.spider,
                request)

