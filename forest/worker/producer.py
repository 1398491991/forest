#coding=utf-8
from scheduler import collectRequestScheduler,collectItemScheduler
from ..utils.serializable import load_json
from ..manager.spider_instance import spiderInstanceManager
from ..manager.slave_info import slaveInfoManager
# import config
import requests
from ..http.response import Response
from ..http.request import Request
# from ..item import Item
from ..utils.select import Selector
import time
import threadpool
from ..xpython import Dict

class WorkRequest(threadpool.WorkRequest):
    def extract_http_request_dict(self):
        return self.args[0]


class ThreadPool(threadpool.ThreadPool):
    def poll(self, block=False):
        """Process any new results in the queue."""
        while True:
            # still results pending?
            if not self.workRequests:
                print 'NoResultsPending'
            # are there still workers to process remaining requests?
            elif block and not self.workers:
                print  'NoWorkersAvailable'
            try:
                # get back next results
                request, result = self._results_queue.get(block=block)
                # has an exception occured?
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
                # hand results to callback, if any
                if request.callback and not \
                       (request.exception and request.exc_callback):
                    request.callback(request, result)
                del self.workRequests[request.requestID]
            except Exception as e:
                print 'error %s'%e
                # break

    def loop(self, block=False):
        return self.poll(block)



BASE_REQUEST_PARAMS=['method','url','headers','files',
    'data','params','auth','cookies','hooks','json',

    'timeout', 'allow_redirects', 'proxies',
    'verify', 'stream', 'cert',
]

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
        print 'task null'
        time.sleep(
            self.get_task_null_sleep_time()
        )

    def get_task_null_sleep_time(self):
        return slaveInfoManager.get_task_null_action_sleep_time()


    def collect_task(self):
        collect_result=self.collectScheduler.collect() # 收集请求进行处理
        return self.make_task(collect_result) if collect_result else self.task_null_action()

    def make_task(self,collect_result):
        # 收集到的都是 json 数据的列表
        for c in collect_result:
            c=load_json(c) # 反序列化
            # assert isinstance(c, dict)
            self.thread_pool.putRequest(
                WorkRequest(
                    self.process_task,
                    (c,), {},
                    callback=self.succ_callback,
                    exc_callback=self.exce_callback
                )

                                        )


    def get_spider_instance(self,spider_name): # 快捷方式
        return spiderInstanceManager.get_spider_instance(spider_name,)

    def get_from_spider_name(self,obj): # 快捷方式
        """获取来自爬虫实例名称"""
        name=obj['from_spider']
        if not name:
            raise Exception,'obj from_spider param is None'
        return name


    # 以下为继承实现
    def process_task(self,obj):
        raise NotImplementedError

    def succ_callback(self,work_request,result):
        print work_request,result

    def exce_callback(self,work_request,result):
        print work_request,result


class ProducerRequest(ProducerBase):

    collectScheduler = collectRequestScheduler


    def process_task(self,request):
        """返回 响应  请求 或者 None """
        # assert isinstance(request,dict)
        # 这里要转换成 Dict 方便使用

        request=Dict(request)

        spider_name=self.get_from_spider_name(request)
        spider_instance=self.get_spider_instance(spider_name)
        mws=spider_instance.mws # todo 待实现
        for mw in mws:
            request=mw.process_request(request)
            if not request:
                # 返回 None 表示放弃这个请求
                break
        if request:
            return self.download_request(request) # download


    def succ_callback(self,work_request,result):
        # 回调请求
        # assert isinstance(work_request,WorkRequest)
        request=work_request.extract_http_request_dict()
        if isinstance(result,Response):
            spider_name=request['from_spider']
            spider_instance=spiderInstanceManager.get_spider_instance(spider_name,)
            return getattr(spider_instance,request['callback'])(result)
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
            return self.bind_select(response,request)

    def bind_select(self,response,request):
        """绑定对象到响应 request 也许解码会用到"""
        select=Selector(response.text,base_url=response.url)
        return Response(response,select)


class ProducerItem(ProducerBase):
    """消费 item 请求"""
    collectScheduler = collectItemScheduler

    def process_task(self,item):
        # assert isinstance(item,dict)

        # 这里要转换成 Dict 方便使用

        item=Dict(item)


        spider_name=self.get_from_spider_name(item)
        spider_instance=self.get_spider_instance(spider_name)

        pipe=spider_instance.pipe
        for pip in pipe:
            item=pip.process_item(item)
            if not item:
                # 返回 None 表示处理完毕
                break

