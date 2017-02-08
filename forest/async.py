#coding=utf-8
from functools import wraps
from http.request import Request
from http.response import Response
from item import Item
import consumer

from spider.info import getSpiderInfo


class Async(object):

    def __call__(self, func):

        def __call(__self, obj):
            if not obj or isinstance(obj,Item):
                return

            res=[]
            if isinstance(obj,Response):
                res=func(__self,obj) # 执行解析方法
                if not isinstance(res,(list,tuple)):
                    res=[res]

            elif isinstance(obj,Request):# 无用的请求 再次
                res=[obj]

            for obj in res: # 针对结果 异步处理
                if not obj.from_spider:
                    obj.from_spider=__self.name
                self.apply_async(obj)

        return __call



    def apply_async(self ,obj):
        if not self.allow_async(obj):
            print "don't allow ,type or spider_name "
            return

        async_optional=obj.async_optional
        return consumer.consumer.process.apply_async(args=(consumer.consumer ,obj,), # ?
                                                  kwargs={},
                                                  **async_optional
                                                  )

    def allow_async(self,obj):
        """判断该对象是否允许处理 主要判断 from_spider"""
        return isinstance(obj,(Request,Item)) and obj.from_spider in getSpiderInfo.get_all_spider_name()



async=Async()