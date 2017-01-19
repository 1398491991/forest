#coding=utf8
from ..http.request import SimpleRequest
from ..item import SimpleItem
from ..static import *




class EnqueueScheduler(object):

    def scheduler(self,obj):
        if isinstance(obj,SimpleRequest):
            # 入队
            if obj.appoint_name:
                return queue.push(appoint_queue_key,obj.to_json())

            if obj.priority:
                priority=obj.priority*-1
                return priority_queue.push(public_priority_queue_key,obj.to_json(),priority=priority)

            return queue.push(public_queue_key,obj.to_json())

        if isinstance(obj,SimpleItem):
            pass

enqueue_scheduler=EnqueueScheduler()

