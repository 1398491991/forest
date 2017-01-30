#coding=utf8
import signal
import os
from ..worker.producer import Producer
from ..compat import frange
import config
from ..utils.misc import get_host_name
from ..rd import rd_conn
from ..worker.scheduler import jobHandoverScheduler

HOST_NAME=get_host_name()

APPOINT_QUEUE_ITEM_KEY=config.APPOINT_QUEUE_ITEM_KEY%{'hostname':HOST_NAME}
PID_SET_KEY=config.PID_SET_KEY%{'hostname':HOST_NAME}


class Slave(object):
    """开启消费者或者关闭消费者"""
    def start(self,hostname,process_count):
        """主机名称 和 需要开启进程个数"""
        ps=[Producer() for _ in frange(process_count)]
        map(lambda p:p.start(),ps)



    def close(self,job_handover=True):
        """完全关闭此 slave ,是否交接任务  将自己的委托队列转换给其他 slave 处理"""
        pid_set=rd_conn.smembers(PID_SET_KEY)
        for pid in pid_set:
            try:
                os.kill(pid,signal.CTRL_C_EVENT)
            except:
                pass
        if job_handover:
            jobHandoverScheduler.job_handover()


    def kill(self,pid,job_handover=False):
        os.kill(pid,signal.CTRL_C_EVENT)
        if job_handover:
            jobHandoverScheduler.job_handover()

    def get_pid_set(self,hostname):
        return rd_conn.smembers()

    def save_pid(self,):
        """保存 pid 到 json 文件
        {"main":xxx,"child":[xxx,xxx,xxx]}
        """

