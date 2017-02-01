#coding=utf-8
from ..rd import rd_conn
import multiprocessing
import config
from producer import ProducerRequest,ProducerItem
import threading
from ..manager.slave_info import slaveInfoManager


LOCAL_HOST_NAME=config.LOCAL_HOST_NAME

JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY
JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY

LOCAL_JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY%{'hostname':LOCAL_HOST_NAME}
LOCAL_JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY%{'hostname':LOCAL_HOST_NAME}

class JobBaseProcess(multiprocessing.Process):
    LOCAL_JOB_PID_KEY=''
    producerClass=None

    def run(self):
        # self.pid_to_redis()
        producerObj=self.producerClass(
            self.get_producer_pool_size()
        )
        t=threading.Thread(target=producerObj.thread_pool.poll,args=(True,))
        t.start()
        producerObj.loop()
        # t.join()

    def get_producer_pool_size(self):
        """ 这是一个快捷方式  关于 slave 即 单次最大并发量"""
        raise NotImplementedError


class JobItemProcess(JobBaseProcess):
    LOCAL_JOB_PID_KEY=LOCAL_JOB_ITEM_PID_KEY
    producerClass=ProducerItem

    def get_producer_pool_size(self):
        return slaveInfoManager.get_parallel_producer_item_size()


class JobRequestProcess(JobBaseProcess):
    LOCAL_JOB_PID_KEY=LOCAL_JOB_REQUEST_PID_KEY
    producerClass=ProducerRequest

    def get_producer_pool_size(self):
        return slaveInfoManager.get_parallel_producer_request_size()