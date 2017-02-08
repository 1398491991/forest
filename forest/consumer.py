#coding=utf8

from celery import Celery
from forest.http.request import Request
from forest.http.response import Response
from forest.utils.select import Selector
from forest.item import Item
from forest.manager.spider_instance import spiderInstanceManager
import requests

BASE_REQUEST_PARAMS=['method','url','headers','files',
    'data','params','auth','cookies','hooks','json',

    'timeout', 'allow_redirects', 'proxies',
    'verify', 'stream', 'cert',
]

EXTEND_REQUEST_PARAMS=['from_spider','encoding','callback','replace_optional',
                 'priority','async_optional','meta',]


app=Celery(__name__,broker='redis://10.0.0.12:6379/0')

class Consumer(object):

    @app.task
    def process(self,obj):
        if isinstance(obj,Request):
            return self.process_request(obj)

        if isinstance(obj,Item):
            return self.process_item(obj)


    def get_spider_instance(self,obj):
        return spiderInstanceManager.get_spider_instance(obj.from_spider)

    def process_request(self,request):
        spider_instance=self.get_spider_instance(request)
        mws=spider_instance.mws
        for mw in mws:
            request=mw.process_request(request)
            if not request:
                # 返回 None 表示放弃这个请求
                return

        res=self.download_request(request) # download

        return self.callback(res)


    def download_request(self,request):
        """只有正确的才能请求  否则就不会再次异步 """
        kwargs = {k:request[k] for k in BASE_REQUEST_PARAMS}
        try:
            response = requests.request(**kwargs)
        except:
            return request
        else:
            map(lambda x:setattr(response,x,request[x]),EXTEND_REQUEST_PARAMS)
            bind_response=self.bind_select(response,request)
            return bind_response

    def bind_select(self,response,request):
        """绑定对象到响应 request 也许解码会用到"""
        select=Selector(response.text,base_url=response.url)
        return Response(response,select)


    def callback(self,obj):
        # 回调请求
        # assert isinstance(work_request,WorkRequest)
        spider_instance=self.get_spider_instance(obj)
        print 213414145
        return getattr(spider_instance,obj.callback)(obj)



    def process_item(self,item):
        spider_instance=self.get_spider_instance(item)
        pipe=spider_instance.pipe
        for pip in pipe:
            item=pip.process_item(item)
            if not item:
                # 返回 None 表示处理完毕
                break

consumer=Consumer()