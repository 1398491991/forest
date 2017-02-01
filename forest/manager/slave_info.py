#coding=utf-8
from ..rd import rd_conn
import config

PARALLEL_PRODUCER_REQUEST_SIZE_KEY=config.PARALLEL_PRODUCER_REQUEST_SIZE_KEY # 最大单次请求处理数量 来自 redis
PARALLEL_PRODUCER_ITEM_SIZE_KEY=config.PARALLEL_PRODUCER_ITEM_SIZE_KEY # 最大单次 item 处理数量 来自 redis
DEFAULT_PARALLEL_PRODUCER_REQUEST_SIZE=config.DEFAULT_PARALLEL_PRODUCER_REQUEST_SIZE # 默认最大请求处数量
DEFAULT_PARALLEL_PRODUCER_ITEM_SIZE=config.DEFAULT_PARALLEL_PRODUCER_ITEM_SIZE # 默认单次 item 最大处理数量

PARALLEL_JOB_ITEM_SIZE_KEY=config.PARALLEL_JOB_ITEM_SIZE_KEY
PARALLEL_JOB_REQUEST_SIZE_KEY=config.PARALLEL_JOB_REQUEST_SIZE_KEY
DEFAULT_PARALLEL_JOB_REQUEST_SIZE=config.DEFAULT_PARALLEL_JOB_REQUEST_SIZE
DEFAULT_PARALLEL_JOB_ITEM_SIZE=config.DEFAULT_PARALLEL_JOB_ITEM_SIZE

JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY
JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY


LOCAL_HOST_NAME=config.LOCAL_HOST_NAME



class SlaveInfoManager(object):
    """获取slave 的一些信息的实现类"""
    hostname=LOCAL_HOST_NAME


    @property
    def rd_conn(self):
        return rd_conn


    def get_parallel_producer_request_size(self):
        c=self.rd_conn.get(PARALLEL_PRODUCER_REQUEST_SIZE_KEY%{"hostname":self.hostname})
        try:
            return int(c)
        except TypeError:
            return DEFAULT_PARALLEL_PRODUCER_REQUEST_SIZE

    def get_parallel_producer_item_size(self):
        c=self.rd_conn.get(PARALLEL_PRODUCER_ITEM_SIZE_KEY%{"hostname":self.hostname})
        try:
            return int(c)
        except TypeError:
            return DEFAULT_PARALLEL_PRODUCER_ITEM_SIZE

    def set_parallel_producer_request_size(self,c):
        assert isinstance(c,int) and c>0

        return self.rd_conn.set(PARALLEL_PRODUCER_ITEM_SIZE_KEY%{"hostname":self.rd_conn},c)


    def set_parallel_producer_item_size(self,c):
        assert isinstance(c,int) and c>0

        return self.rd_conn.set(PARALLEL_PRODUCER_REQUEST_SIZE_KEY%{"hostname":self.hostname},c)


    def get_parallel_job_request_size(self):
        c=self.rd_conn.get(PARALLEL_JOB_REQUEST_SIZE_KEY%{"hostname":self.hostname})
        try:
            return int(c)
        except TypeError:
            return DEFAULT_PARALLEL_JOB_REQUEST_SIZE


    def get_parallel_job_item_size(self):
        c=self.rd_conn.get(PARALLEL_JOB_ITEM_SIZE_KEY%{"hostname":self.hostname})
        try:
            return int(c)
        except TypeError:
            return DEFAULT_PARALLEL_JOB_ITEM_SIZE


    def get_parallel_job_item_pids(self):
        return self.rd_conn.smembers(JOB_ITEM_PID_KEY%{"hostname":self.hostname})


    def get_parallel_job_request_pids(self):
        return self.rd_conn.smembers(JOB_REQUEST_PID_KEY%{"hostname":self.hostname})

    def re_hostname(self,hostname):
        self.hostname=hostname



slaveInfoManager=SlaveInfoManager() # 全部指的是本地