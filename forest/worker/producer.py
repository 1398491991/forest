#coding=utf-8
from .thread import ThreadPool
from scheduler import collectRequestScheduler,collectItemScheduler
from ..utils.serializable import load_json,load_pickle,dump_pickle
from ..rd import rd_conn
import config
import requests
from ..http.response import Response
from ..http.request import Request
from ..item import Item
from ..utils.select import Selector

BASE_REQUEST_PARAMS=['method','url','headers','files',
    'data','params','auth','cookies','hooks','json',]

EXTEND_REQUEST_PARAMS=['from_spider','callback','project_path','replace_optional',
                 'priority','appoint_name','meta',]


SPIDER_INSTANCE_KEY=config.SPIDER_INSTANCE_KEY

# thread_pool=threadpool.ThreadPool(5)

class SpiderInstanceManager(object):
    """管理spider 实例"""
    def get_spider_instance(self,spider_name,to_obj=True,
                            local_copy=True):
        attr='spider_%s'%spider_name
        if hasattr(self,attr):
            return getattr(self,attr)
        try:
            key=SPIDER_INSTANCE_KEY%{'spider_name':spider_name}
            spider_instance=rd_conn.get(key)
            if to_obj:
                spider_instance=load_pickle(spider_instance)
            if local_copy:
                setattr(self,attr,spider_instance)

            return spider_instance

        except ImportError:
            return None

    def set_spider_instance(self,spider_name,spider_instance,
                            to_pickle=True):
        """将 spider 设置到 redis 中"""
        key=SPIDER_INSTANCE_KEY%{'spider_name':spider_name}
        if rd_conn.exists(key):
            raise Exception
        if to_pickle:
            spider_instance=dump_pickle(spider_instance)
        return rd_conn.set(key,spider_instance)


spiderInstanceManager=SpiderInstanceManager()






class ProducerRequest(object):
    """消费http请求"""
    def __init__(self,thread_pool_or_size):
        if isinstance(thread_pool_or_size,int):
            thread_pool_or_size=ThreadPool(thread_pool_or_size)

        self.thread_pool=thread_pool_or_size

    def producer(self):
        while 1:
            self.producer_request()


    def producer_request(self):
        collect=collectRequestScheduler.collect() # 收集请求处理
        # 收集到的都是 json数据
        print 'collect %s'%collect
        for c in collect:
            c=load_json(c) # 反序列化
            task = self.thread_pool.makeRequests(self.process_request,
                                           ((c,),{}), self.callback_request, None)
            self.thread_pool.putRequest(task,)


    def process_request(self,request):
        spider_name=request.get('from_spider')
        if not spider_name:
            raise Exception

        spider_instance=spiderInstanceManager.get_spider_instance(spider_name,)
        # pipe=spider_instance.pipe
        mws=spider_instance.mws
        for mw in mws:
            request=mw.process_request(request)
            if not request:
                # 返回 None 表示放弃这个请求
                break

        return self.download_request(request) # download

    def download_request(self,request):
        """只有正确的才能请求  否则就不会再次异步 """
        if request:
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

    def callback_request(self,request,result):
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


class ProducerItem(object):
    """消费http请求"""
    def __init__(self,thread_pool_or_size):
        if isinstance(thread_pool_or_size,int):
            thread_pool_or_size=ThreadPool(thread_pool_or_size)

        self.thread_pool=thread_pool_or_size


    def producer(self):
        while 1:
            self.producer_item()

    def producer_item(self):
        collect=collectItemScheduler.collect() # 收集请求处理
        # 收集到的都是 json 数据
        for c in collect:
            c=load_json(c) # 反序列化
            task = self.thread_pool.makeRequests(self.process_item,
                                           ((c,),{}), None, None)
            self.thread_pool.putRequest(task,)


    def process_item(self,item):
        # assert isinstance(item,dict)
        spider_name=item.get('from_spider')
        if not spider_name:
            raise Exception

        spider_instance=spiderInstanceManager.get_spider_instance(spider_name,)
        pipe=spider_instance.pipe
        # mws=spider_instance.mws
        for pip in pipe:
            item=pip.process_item(item)
            if not item:
                # 返回 None 表示完毕
                break
        if item:
            return self.save_item(Item(item))

    def save_item(self,item):
        """存储 item  """
        # assert isinstance(item,Item)
        raise NotImplementedError