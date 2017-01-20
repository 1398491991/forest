#coding=utf8
import signal
import os
from ..worker.producer import Producer

class Slave(object):
    """开启消费者或者关闭消费者"""
    def start(self,hostname,process_count):
        """主机名称 和 需要开启进程个数"""
        pass

    def close(self,pid,job_handover=True):
        """完全关闭此 slave ,是否交接任务  将自己的委托队列转换给其他 slave 处理"""
        pass

    def kill(self,pid,job_handover=False):
        pass

    def get_pid(self,hostname):
        pass

    def save_pid(self,):
        """保存 pid 到 json 文件
        {"main":xxx,"child":[xxx,xxx,xxx]}
        """

