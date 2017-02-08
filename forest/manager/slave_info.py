#coding=utf-8
from ..rd import rd_conn
import forest_config

PARALLEL_PRODUCER_REQUEST_COUNT_KEY=forest_config.PARALLEL_PRODUCER_REQUEST_COUNT_KEY # 最大单次请求处理数量 来自 redis
PARALLEL_PRODUCER_ITEM_COUNT_KEY=forest_config.PARALLEL_PRODUCER_ITEM_COUNT_KEY # 最大单次 item 处理数量 来自 redis
DEFAULT_PARALLEL_PRODUCER_REQUEST_COUNT=forest_config.DEFAULT_PARALLEL_PRODUCER_REQUEST_COUNT # 默认最大请求处数量
DEFAULT_PARALLEL_PRODUCER_ITEM_COUNT=forest_config.DEFAULT_PARALLEL_PRODUCER_ITEM_COUNT # 默认单次 item 最大处理数量

PARALLEL_JOB_ITEM_COUNT_KEY=forest_config.PARALLEL_JOB_ITEM_COUNT_KEY
PARALLEL_JOB_REQUEST_COUNT_KEY=forest_config.PARALLEL_JOB_REQUEST_COUNT_KEY
DEFAULT_PARALLEL_JOB_REQUEST_COUNT=forest_config.DEFAULT_PARALLEL_JOB_REQUEST_COUNT
DEFAULT_PARALLEL_JOB_ITEM_COUNT=forest_config.DEFAULT_PARALLEL_JOB_ITEM_COUNT

JOB_REQUEST_PID_KEY=forest_config.JOB_REQUEST_PID_KEY
JOB_ITEM_PID_KEY=forest_config.JOB_ITEM_PID_KEY

DEFAULT_TASK_NULL_ACTION_SLEEP_TIME=forest_config.DEFAULT_TASK_NULL_ACTION_SLEEP_TIME
TASK_NULL_ACTION_SLEEP_TIME_KEY=forest_config.TASK_NULL_ACTION_SLEEP_TIME_KEY

SLAVE_NAMES_KEY=forest_config.SLAVE_NAMES_KEY

LOCAL_HOST_NAME=forest_config.LOCAL_HOST_NAME



class SlaveInfoManager(object):
    """获取slave 的一些信息的实现类"""
    hostname=LOCAL_HOST_NAME


    @property
    def rd_conn(self):
        return rd_conn

    @property
    def hostname_map(self):
        return {"hostname": self.hostname}


    def get_parallel_producer_request_count(self):
        """无法改变，除非重启重新设定"""
    #     c=self.rd_conn.get(PARALLEL_PRODUCER_REQUEST_COUNT_KEY%self.hostname_map)
    #     try:
    #         return int(c)
    #     except TypeError:
        return DEFAULT_PARALLEL_PRODUCER_REQUEST_COUNT

    def get_parallel_producer_item_count(self):
        """无法改变的"""
        # c=self.rd_conn.get(PARALLEL_PRODUCER_ITEM_COUNT_KEY%self.hostname_map)
        # try:
        #     return int(c)
        # except TypeError:
        return DEFAULT_PARALLEL_PRODUCER_ITEM_COUNT

    # def set_parallel_producer_request_size(self,c):
    #     assert isinstance(c,int) and c>0
    #
    #     return self.rd_conn.set(PARALLEL_PRODUCER_ITEM_COUNT_KEY%self.hostname_map,c)
    #
    #
    # def set_parallel_producer_item_size(self,c):
    #     assert isinstance(c,int) and c>0
    #
    #     return self.rd_conn.set(PARALLEL_PRODUCER_REQUEST_COUNT_KEY%self.hostname_map,c)

    def set_task_null_action_sleep_time(self,t=DEFAULT_TASK_NULL_ACTION_SLEEP_TIME):
        assert isinstance(t,(int,float)) and t>0
        return self.rd_conn.set(TASK_NULL_ACTION_SLEEP_TIME_KEY,t)


    def get_parallel_job_request_count(self):
        return len(self.get_parallel_job_request_pids())
        # c=self.rd_conn.get(PARALLEL_JOB_REQUEST_COUNT_KEY%self.hostname_map)
        # try:
        #     return int(c)
        # except TypeError:
        #     return DEFAULT_PARALLEL_JOB_REQUEST_COUNT


    def get_parallel_job_item_count(self):
        return len(self.get_parallel_job_item_pids())
        # c=self.rd_conn.get(PARALLEL_JOB_ITEM_COUNT_KEY%self.hostname_map)
        # try:
        #     return int(c)
        # except TypeError:
        #     return DEFAULT_PARALLEL_JOB_ITEM_COUNT


    def get_parallel_job_item_pids(self):
        return self.rd_conn.smembers(JOB_ITEM_PID_KEY%self.hostname_map)


    def get_parallel_job_request_pids(self):
        return self.rd_conn.smembers(JOB_REQUEST_PID_KEY%self.hostname_map)

    def re_hostname(self,hostname):
        self.hostname=hostname

    def get_task_null_action_sleep_time(self):
        res=self.rd_conn.get(TASK_NULL_ACTION_SLEEP_TIME_KEY)
        try:
            return float(res)
        except TypeError:
            return DEFAULT_TASK_NULL_ACTION_SLEEP_TIME


    def get_all_slave_names(self):
        return self.rd_conn.smembers(SLAVE_NAMES_KEY)



slaveInfoManager=SlaveInfoManager() # 全部指的是本地