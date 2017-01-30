#coding=utf-8
from .worker import ThreadPool
from scheduler import collectRequestScheduler,collectItemScheduler
from ..utils.serializable import load_json
from ..worker import spiderInstanceManager
# import config
import requests
from ..http.response import Response
from ..http.request import Request
# from ..item import Item
from ..utils.select import Selector
import time


BASE_REQUEST_PARAMS=['method','url','headers','files',
    'data','params','auth','cookies','hooks','json',]

EXTEND_REQUEST_PARAMS=['from_spider','callback','project_path','replace_optional',
                 'priority','appoint_name','meta',]


class ProducerBase(object):
    collectScheduler=None

    def __init__(self,thread_pool_size):
        assert isinstance(thread_pool_size,int)
        self.thread_pool=ThreadPool(thread_pool_size)

    def loop(self):
        while 1:
            self.collect_task()

    def task_null_action(self):
        # 当收集结果为 空 list 时候 进行的动作
        print 'sleep'
        time.sleep(5)


    def collect_task(self):
        collect_result=self.collectScheduler.collect() # 收集请求进行处理
        return self.make_task(collect_result) if collect_result else self.task_null_action()

    def make_task(self,collect_result):
        # 收集到的都是 json 数据的列表
        for c in collect_result:
            c=load_json(c) # 反序列化
            task = self.thread_pool.makeRequests(self.process_task,
                                                ((c,),{}),
                                                 self.succ_callback,
                                                 self.exce_callback
                                                 )
            self.thread_pool.putRequest(task,)


    def get_spider_instance(self,spider_name): # 快捷方式
        return spiderInstanceManager.get_spider_instance(spider_name,)

    def get_from_spider_name(self,obj): # 快捷方式
        """获取来自爬虫实例名称"""
        name=obj['from_spider']
        if not name:
            raise Exception


    # 以下为继承实现
    def process_task(self,obj):
        raise NotImplementedError

    def succ_callback(self,obj,result):
        pass

    def exce_callback(self,obj,result):
        pass


class ProducerRequest(ProducerBase):

    collectScheduler = collectRequestScheduler


    def process(self,request):
        """返回 响应  请求 或者 None """
        # assert isinstance(request,dict)
        spider_name=self.get_from_spider_name(request)
        spider_instance=self.get_spider_instance(spider_name)

        mws=spider_instance.mws
        for mw in mws:
            request=mw.process_request(request)
            if not request:
                # 返回 None 表示放弃这个请求
                break

        if request:
            return self.download_request(request) # download


    def succ_callback(self,request,result):
        # 回调请求
        if isinstance(result,Response):
            spider_name=request.get('from_spider')
            if not spider_name:
                raise Exception
            spider_instance=spiderInstanceManager.get_spider_instance(spider_name,)
            return getattr(spider_instance,result['callback'])(result)

        if isinstance(result,Request):# 原路返回 再次分发
            return result

        return None # 什么都不是



    def download_request(self,request):
        """只有正确的才能请求  否则就不会再次异步 """
        kwargs = {k:request[k] for k in BASE_REQUEST_PARAMS}
        try:
            response = requests.request(**kwargs)
        except:
            return Request(**request)
        else:
            map(lambda x:setattr(response,x,request[x]),EXTEND_REQUEST_PARAMS)
            return self.bind(response,request)

    def bind(self,response,request):
        """绑定对象到响应 request 也许解码会用到"""
        select=Selector(response.text,base_url=response.url)
        return Response(response,select)


class ProducerItem(ProducerBase):
    """消费 item 请求"""
    collectScheduler = collectItemScheduler

    def process_task(self,item):
        # assert isinstance(item,dict)
        spider_name=self.get_from_spider_name(item)
        spider_instance=self.get_spider_instance(spider_name)

        pipe=spider_instance.pipe
        for pip in pipe:
            item=pip.process_item(item)
            if not item:
                # 返回 None 表示处理完毕
                break

