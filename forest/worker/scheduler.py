#coding=utf8
# from ..http.request import SimpleRequest
# from ..item import SimpleItem
# from ..static import *
from ..compat import frange
from ..queue import plainQueue,priorityQueue #,stackQueue
from ..slave.info import slaveInfo
from ..utils.misc import get_host_name
import config

HOST_NAME=get_host_name()

LOCAL_APPOINT_QUEUE_REQUEST_KEY=config.APPOINT_QUEUE_REQUEST_KEY%{'hostname':HOST_NAME}
LOCAL_PUBLIC_PRIORITY_QUEUE_REQUEST_KEY=config.PUBLIC_PRIORITY_QUEUE_REQUEST_KEY%{'hostname':HOST_NAME}
LOCAL_PUBLIC_QUEUE_REQUEST_KEY=config.PUBLIC_QUEUE_REQUEST_KEY%{'hostname':HOST_NAME}

LOCAL_APPOINT_QUEUE_ITEM_KEY=config.APPOINT_QUEUE_ITEM_KEY%{'hostname':HOST_NAME}
LOCAL_PUBLIC_PRIORITY_QUEUE_ITEM_KEY=config.PUBLIC_PRIORITY_QUEUE_ITEM_KEY%{'hostname':HOST_NAME}
LOCAL_PUBLIC_QUEUE_ITEM_KEY=config.PUBLIC_QUEUE_ITEM_KEY%{'hostname':HOST_NAME}

MAX_PROCESS_COUNT_KEY=config.MAX_PROCESS_COUNT_KEY





class EnqueueBaseScheduler(object):
    def enqueue(self,obj,handover=False):
        raise NotImplementedError


class EnqueueRequestScheduler(EnqueueBaseScheduler):
    """将各种需求和不同类型分发到不同的队列中"""

    def enqueue(self,request,handover=False):
        # assert isinstance(request,SimpleRequest)
        # 入队
        if request.appoint_name==HOST_NAME and not handover:# 交接过程（本 slave close）不能入队 appoint 限制:
            return plainQueue.push(APPOINT_QUEUE_REQUEST_KEY,request.to_json(),x=True) # 列表不存在跳过此过程

        if request.priority:
            priority=request.priority*-1
            return priorityQueue.push(PUBLIC_PRIORITY_QUEUE_REQUEST_KEY,request.to_json(),priority=priority)

        return plainQueue.push(PUBLIC_QUEUE_REQUEST_KEY,request.to_json())


class EnqueueItemScheduler(EnqueueBaseScheduler):

    def enqueue(self,item,handover=False):

        if item.appoint_name==HOST_NAME and not handover:# 交接过程不能入队 appoint 限制
            return plainQueue.push(APPOINT_QUEUE_ITEM_KEY,item.to_json(),x=True)

        if item.priority:
            priority=item.priority*-1
            return priorityQueue.push(PUBLIC_PRIORITY_QUEUE_ITEM_KEY,item.to_json(),priority=priority)

        return plainQueue.push(PUBLIC_QUEUE_ITEM_KEY,item.to_json())





class CollectBaseScheduler(object):

    def _collect(self,queue_instance,key,count):
        """从不同队列取出对象 按照 count 的个数 ， count <=0 all 主要用于 交接过程"""
        if count<=0:
            # 返回全部 一般适用于交接过程
            pipe=queue_instance.pipeline()
            pipe.multi()
            collect=pipe.lrange(key,0,-1)
            pipe.delete(key)
            pipe.execute()
            return collect


        collect=[]
        for _ in frange(count):
            obj=queue_instance.pop(key)
            if obj:
                collect.append(obj)
        return collect

    def handover_collect(self):
        return NotImplementedError



    def collect(self,count=None):
        raise NotImplementedError


class CollectRequestScheduler(CollectBaseScheduler):
    """按照指定的个数 从不同队列收集 需要处理的对象信息"""

    def collect(self,count=None):
        count=count or slaveInfo.get_max_process_request_count(HOST_NAME)
        collect=[]
        collect+=self.collect_appoint_request(count)
        collect+=self.collect_public_priority_request(count-len(collect))
        collect+=self.collect_public_request(count-len(collect))
        return collect

    def handover_collect(self):
        return self._collect(plainQueue,LOCAL_APPOINT_QUEUE_REQUEST_KEY,-1)

    def collect_appoint_request(self,count):
        """收集委托的 请求"""
        return self._collect(plainQueue,LOCAL_APPOINT_QUEUE_REQUEST_KEY,count)

    def collect_public_priority_request(self,count):
        return self._collect(priorityQueue,LOCAL_PUBLIC_PRIORITY_QUEUE_REQUEST_KEY,count)

    def collect_public_request(self,count):
        return self._collect(plainQueue,LOCAL_PUBLIC_QUEUE_REQUEST_KEY,count)


class CollectItemScheduler(CollectBaseScheduler):


    def collect(self,count=None):
        count=count or slaveInfo.get_max_process_item_count(HOST_NAME)
        collect=[]
        collect+=self.collect_appoint_item(count)
        collect+=self.collect_public_priority_item(count-len(collect))
        collect+=self.collect_public_item(count-len(collect))
        return collect

    def handover_collect(self):
        return self._collect(plainQueue,APPOINT_QUEUE_ITEM_KEY,-1)

    def collect_appoint_item(self,count):
        """收集委托的 请求"""
        return self._collect(plainQueue,APPOINT_QUEUE_ITEM_KEY,count)

    def collect_public_priority_item(self,count):
        return self._collect(priorityQueue,PUBLIC_PRIORITY_QUEUE_ITEM_KEY,count)

    def collect_public_item(self,count):
        return self._collect(plainQueue,PUBLIC_QUEUE_ITEM_KEY,count)

enqueueRequestScheduler=EnqueueRequestScheduler()
enqueueItemScheduler=EnqueueItemScheduler()
collectItemScheduler=CollectItemScheduler()
collectRequestScheduler=CollectRequestScheduler()


class JobHandoverScheduler(object):
    """工作移交"""
    def job_handover(self):
        map(enqueueRequestScheduler.enqueue,collectRequestScheduler.handover_collect())
        map(enqueueItemScheduler.enqueue,collectItemScheduler.handover_collect())

jobHandoverScheduler=JobHandoverScheduler()


