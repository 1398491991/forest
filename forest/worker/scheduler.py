#coding=utf8
# from ..http.request import SimpleRequest
# from ..item import SimpleItem
# from ..static import *
from ..compat import frange
from ..queue import plainQueue,priorityQueue #,stackQueue
from ..slave.info import slaveInfo
import config

LOCAL_HOST_NAME=config.LOCAL_HOST_NAME

APPOINT_QUEUE_REQUEST_KEY=config.APPOINT_QUEUE_REQUEST_KEY
PUBLIC_PRIORITY_QUEUE_REQUEST_KEY=config.PUBLIC_PRIORITY_QUEUE_REQUEST_KEY
PUBLIC_QUEUE_REQUEST_KEY=config.PUBLIC_QUEUE_REQUEST_KEY

APPOINT_QUEUE_ITEM_KEY=config.APPOINT_QUEUE_ITEM_KEY
PUBLIC_PRIORITY_QUEUE_ITEM_KEY=config.PUBLIC_PRIORITY_QUEUE_ITEM_KEY
PUBLIC_QUEUE_ITEM_KEY=config.PUBLIC_QUEUE_ITEM_KEY

MAX_PROCESS_COUNT_KEY=config.MAX_PROCESS_COUNT_KEY





class EnqueueBaseScheduler(object):
    PUBLIC_PRIORITY_QUEUE_KEY=''
    PUBLIC_QUEUE_KEY=''
    APPOINT_QUEUE_KEY=''

    def enqueue(self,obj,handover=False,handover_host_name=None):
        """如果 handover 为 True 则不会进入 local 委托队列 默认委托本地队列"""
        # 入队
        if handover:# 委托为True
            # assert handover_host_name # 当 handover 为 真 那么 handover_host_name 一定要指定
            if obj.appoint_name==handover_host_name:# 委托的队列刚好是这个
                return self.enqueue_to_public_priority(obj) # 进入优先级的队列
            else:#委托名称不对应 可以入队列
                return self.enqueue_to_appoint(obj)
        elif obj.priority:# 优先级委托
            return self.enqueue_to_public_priority(obj)
        else:
            return self.enqueue_to_public(obj) # 平凡的

    def enqueue_to_appoint(self,obj):
        # 最高待遇的
        res=plainQueue.push(self.APPOINT_QUEUE_KEY%{'hostname':obj.appoint_name},
                            obj.to_json(),x=True)
        if not res:#入队失败
            return self.enqueue_to_public_priority(obj) # 进入优先级队列
        return True

    def enqueue_to_public(self,obj):
        res=plainQueue.push(self.PUBLIC_QUEUE_KEY,obj.to_json())
        if not res:
            # 警告
            return False
        return True

    def enqueue_to_public_priority(self,obj):
        if obj.priority:
            priority=obj.priority*-1
            res=priorityQueue.push(self.PUBLIC_PRIORITY_QUEUE_KEY,
                                   obj.to_json(),priority=priority)
            if not res:
                return self.enqueue_to_public(obj)
            return True


class EnqueueRequestScheduler(EnqueueBaseScheduler):
    """将各种需求和不同类型分发到不同的队列中"""
    PUBLIC_PRIORITY_QUEUE_KEY=PUBLIC_PRIORITY_QUEUE_REQUEST_KEY
    PUBLIC_QUEUE_KEY=PUBLIC_QUEUE_REQUEST_KEY
    APPOINT_QUEUE_KEY=APPOINT_QUEUE_REQUEST_KEY
    # assert isinstance(request,SimpleRequest)


class EnqueueItemScheduler(EnqueueBaseScheduler):

    PUBLIC_PRIORITY_QUEUE_KEY=PUBLIC_PRIORITY_QUEUE_ITEM_KEY
    PUBLIC_QUEUE_KEY=PUBLIC_QUEUE_ITEM_KEY
    APPOINT_QUEUE_KEY=APPOINT_QUEUE_ITEM_KEY
    # assert isinstance(item,Item)





class CollectBaseScheduler(object):
    """单例模式吧"""
    PUBLIC_PRIORITY_QUEUE_KEY=''
    PUBLIC_QUEUE_KEY=''
    APPOINT_QUEUE_KEY=''


    def _collect(self,queue_instance,key,count):
        """从不同队列取出对象 按照 count 的个数 ， count <=0 all 主要用于 交接过程"""
        if count<0:
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

    def collect(self,count=None,collect_host_name=LOCAL_HOST_NAME):
        count=count or self.get_max_process_count(collect_host_name)
        # assert count
        collect=[]
        collect+=self.collect_appoint_request(count,collect_host_name)
        collect+=self.collect_public_priority_request(count-len(collect))
        collect+=self.collect_public_request(count-len(collect))
        return collect

    def handover_collect(self,collect_host_name=LOCAL_HOST_NAME):
        return self._collect(plainQueue,self.APPOINT_QUEUE_KEY%{'hostname':collect_host_name},-1)

    def collect_appoint_request(self,count,collect_host_name=LOCAL_HOST_NAME):
        """收集委托的 请求"""
        return self._collect(plainQueue,self.APPOINT_QUEUE_KEY%{'hostname':collect_host_name},
                             count)

    def collect_public_priority_request(self,count):
        return self._collect(priorityQueue,self.PUBLIC_PRIORITY_QUEUE_KEY,count)

    def collect_public_request(self,count):
        return self._collect(plainQueue,self.PUBLIC_QUEUE_KEY,count)


    def get_max_process_count(self,collect_host_name=LOCAL_HOST_NAME):
        raise NotImplementedError


class CollectRequestScheduler(CollectBaseScheduler):
    """按照指定的个数 从不同队列收集 需要处理的对象信息"""
    PUBLIC_PRIORITY_QUEUE_KEY=PUBLIC_PRIORITY_QUEUE_REQUEST_KEY
    PUBLIC_QUEUE_KEY=PUBLIC_QUEUE_REQUEST_KEY
    APPOINT_QUEUE_KEY=APPOINT_QUEUE_REQUEST_KEY

    def get_max_process_count(self,collect_host_name=LOCAL_HOST_NAME):
        return slaveInfo.get_max_process_request_count(collect_host_name)



class CollectItemScheduler(CollectBaseScheduler):
    PUBLIC_PRIORITY_QUEUE_KEY=PUBLIC_PRIORITY_QUEUE_ITEM_KEY
    PUBLIC_QUEUE_KEY=PUBLIC_QUEUE_ITEM_KEY
    APPOINT_QUEUE_KEY=APPOINT_QUEUE_ITEM_KEY

    def get_max_process_count(self,collect_host_name=LOCAL_HOST_NAME):
        return slaveInfo.get_max_process_item_count(collect_host_name)


enqueueRequestScheduler=EnqueueRequestScheduler()
enqueueItemScheduler=EnqueueItemScheduler()
collectItemScheduler=CollectItemScheduler()
collectRequestScheduler=CollectRequestScheduler()




class JobHandoverScheduler(object):
    """工作移交"""
    def job_handover(self,handover_host_name):
        # 也许需要 事务处理
        map(lambda x:
            enqueueRequestScheduler.enqueue(x,True,handover_host_name),
            collectRequestScheduler.handover_collect(collect_host_name=
                                                     handover_host_name)
            )

        map(lambda x:
            enqueueItemScheduler.enqueue(x,True,handover_host_name),
            collectItemScheduler.handover_collect(collect_host_name=
                                                    handover_host_name)
            )

jobHandoverScheduler=JobHandoverScheduler()


