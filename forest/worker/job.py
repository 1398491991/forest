import multiprocessing
from ..rd import rd_conn
import config
from producer import ProducerRequest,ProducerItem
import threading

LOCAL_HOST_NAME=config.LOCAL_HOST_NAME

JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY
JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY

LOCAL_JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY%{'hostname':LOCAL_HOST_NAME}
LOCAL_JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY%{'hostname':LOCAL_HOST_NAME}


class JobItemProcess(multiprocessing.Process):

    def pid_to_redis(self):
        return rd_conn.sadd(LOCAL_JOB_ITEM_PID_KEY,self.pid)


    def run(self):
        self.pid_to_redis()
        producerItem=ProducerItem(5)
        t1=threading.Thread(target=producerItem.loop,)
        t2=threading.Thread(target=producerItem.thread_pool.poll,args=(True,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

class JobRequestProcess(multiprocessing.Process):

    def pid_to_redis(self):
        rd_conn.sadd(LOCAL_JOB_REQUEST_PID_KEY,self.pid)


    def run(self):
        self.pid_to_redis()
        producerRequest=ProducerRequest(5)
        t1=threading.Thread(target=producerRequest.loop,)
        t2=threading.Thread(target=producerRequest.thread_pool.poll,args=(True,))
        # t1.setDaemon(1)
        # t2.setDaemon(1)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # print 12313
