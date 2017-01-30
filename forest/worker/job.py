import multiprocessing
from ..rd import rd_conn
import sys,os
from forest.utils.parse_config import parseConfig
sys.path.append(os.path.dirname(parseConfig.config_path))
import config
from ..utils.misc import get_host_name
from producer import ProducerRequest,ProducerItem
import threading

HOST_NAME=get_host_name()
JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY
JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY
LOCAL_JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY%{'hostname':HOST_NAME}
LOCAL_JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY%{'hostname':HOST_NAME}


class JobItemProcess(multiprocessing.Process):

    def pid_to_redis(self):
        return rd_conn.sadd(LOCAL_JOB_ITEM_PID_KEY,self.pid)


    def run(self):
        self.pid_to_redis()
        producerItem=ProducerItem(5)
        # threading.Thread(target=producerItem.producer,).start()
        # threading.Thread(target=producerItem.thread_pool.poll,).start()
        t1=threading.Thread(target=producerItem.producer,)
        t2=threading.Thread(target=producerItem.thread_pool.poll,)
        # t1.setDaemon(1)
        # t2.setDaemon(1)
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
        t1=threading.Thread(target=producerRequest.producer,)
        t2=threading.Thread(target=producerRequest.thread_pool.poll,)
        # t1.setDaemon(1)
        # t2.setDaemon(1)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # print 12313
