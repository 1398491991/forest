#coding=utf-8
import multiprocessing
from ..static import *
from ..compat import frange
from send import Send
import time
from ..utils.serializable import load_json,load_pickle


send=Send()
MAX_PROCESS_COUNT=10

class Producer(multiprocessing.Process):
    def run(self):
        while 1:
            # try:
                self.producer()
            # except Exception as e:
            #     print e

    def producer(self):
        collect=self.collect()
        if not collect:
            # sleep
            print 'sleep '
            return time.sleep(2)

        return self.callback(
            self.send(collect)
        )



    def collect(self):
        collect=[]
        collect+=self.collect_appoint_queue(MAX_PROCESS_COUNT)
        collect+=self.collect_public_priority_queue(MAX_PROCESS_COUNT-len(collect))
        collect+=self.collect_public_queue(MAX_PROCESS_COUNT-len(collect))
        return collect

    def mws(self,collect):
        pass

    def send(self,collect):
        return send.map(map(load_json,collect))

    def callback(self,obj):
        def _callback(obj):
            spider=self.get_spider(o['from_spider'])
            if spider:
                # async res=func(self,obj)
               return getattr(spider,o['callback'])(o)

        for o in obj:
            _callback(o)




    def get_spider(self,name):
        attr='spider_%s'%name
        if hasattr(self,attr):
            return getattr(self,attr)
        try:
            spider=load_pickle(rd_conn.get(name))
            setattr(self,attr,spider)
        except ImportError:
            return None


    def __collect_queue(self,queue,key,count):
        collect=[]
        for _ in frange(count):
            obj=queue.pop(key)
            if obj:
                collect.append(obj)
        return collect

    def collect_appoint_queue(self,count):
        """收集委托的 请求"""
        return self.__collect_queue(queue,appoint_queue_key,count)

    def collect_public_priority_queue(self,count):
        return self.__collect_queue(priority_queue,public_priority_queue_key,count)

    def collect_public_queue(self,count):
        return self.__collect_queue(queue,public_queue_key,count)

