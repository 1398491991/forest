#coding=utf8

from celery import Celery
from forest.http.request import Request
from forest.http.response import Response
from forest.utils.select import Selector
from forest.item import Item
from forest.manager.spider_instance import spiderInstanceManager
import requests
import celery_config

BASE_REQUEST_PARAMS=['method','url','headers','files',
    'data','params','auth','cookies','hooks','json',

    'timeout', 'allow_redirects', 'proxies',
    'verify', 'stream', 'cert',
]

EXTEND_REQUEST_PARAMS=['from_spider','encoding','callback','replace_optional',
                 'priority','async_optional','meta',]


app=Celery()
app.config_from_object(celery_config)


class ConsumerBase(object):

    def get_spider_instance(self,obj):
        return spiderInstanceManager.get_spider_instance(obj.from_spider)

    def process(self, obj):
        raise NotImplementedError

class ConsumerRequest(ConsumerBase):

    def process(self, request):
        spider_instance=self.get_spider_instance(request)
        mws=spider_instance.mws
        for mw in mws:
            request=mw.process_request(request)
            if not request:
                # 返回 None 表示放弃这个请求
                return

        response_or_request=self.download_request(request) # download

        return self.callback(response_or_request)


    def download_request(self,request):
        """只有正确的才能请求  否则就不会再次异步 """
        kwargs = {k:request[k] for k in BASE_REQUEST_PARAMS}
        try:
            response = requests.request(**kwargs)
        except Exception as e:
            print 'down load error %s'%e
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
        # 回调
        spider_instance=self.get_spider_instance(obj)
        return getattr(spider_instance,obj.callback)(obj)


class ConsumerItem(ConsumerBase):

    def process(self,item):
        spider_instance=self.get_spider_instance(item)
        pipe=spider_instance.pipe
        for pip in pipe:
            item=pip.process_item(item)
            if not item:
                # 返回 None 表示处理完毕
                break

consumerItem = ConsumerItem()
consumerRequest = ConsumerRequest()

@app.task
def task_route(obj):
    """分发任务"""
    print obj
    return obj
    # if isinstance(obj,Request):
    #     return consumerRequest.process(obj)

    # if isinstance(obj,Item):
    #     return consumerItem.process(obj)

