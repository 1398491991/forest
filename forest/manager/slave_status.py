#coding=utf8
import signal
import os
from ..worker.job import JobItemProcess,JobRequestProcess
from ..compat import frange
import config
from ..rd import rd_conn
from slave_info import slaveInfoManager


LOCAL_HOST_NAME=config.LOCAL_HOST_NAME
APPOINT_QUEUE_ITEM_KEY=config.APPOINT_QUEUE_ITEM_KEY
JOB_REQUEST_PID_KEY=config.JOB_REQUEST_PID_KEY
JOB_ITEM_PID_KEY=config.JOB_ITEM_PID_KEY

class SlaveStatusBaseManager(object):
    jobProcessClass=None
    hostname=LOCAL_HOST_NAME
    JOB_PID_KEY=''



    @property
    def rd_conn(self):
        return rd_conn

    def start(self):

        size=self.get_parallel_job_size()
        assert isinstance(size,int) and size>0
        for _ in frange(size):
            pipe=self.rd_conn.pipeline()
            try:
                p=self.jobProcessClass()
                p.start()
                self.add_pid(pipe,p.pid)
            except Exception as e:
                print 'start error %s'%e
            else:
                pipe.execute()


    def get_parallel_job_size(self):
        raise NotImplementedError

    def get_parallel_job_pids(self):
        raise NotImplementedError

    def close(self):
        pids=self.get_parallel_job_pids()
        # pid type == str
        res={}
        # if not pids:
        #     警告
        for pid in pids:
            res['kill pid_%s'%pid]=self.kill(pid)

        return res


    def kill(self,pid):
        pipe=self.rd_conn.pipeline()
        try:
            pid=int(pid)
            os.kill(pid,signal.SIGINT) # 暂时的
        # except WindowsError
        except Exception as e:
            print e
            return False
        else:
            self.rm_pid(pipe,pid)
            pipe.execute()
            return True


    def rm_pid(self,pipe,pid):
        # pipe=self.rd_conn.pipeline()
        assert isinstance(pid,int)
        pipe.srem(self.JOB_PID_KEY%{'hostname':self.hostname},pid)

    def add_pid(self,pipe,pid):
        # pipe=self.rd_conn.pipeline()
        assert isinstance(pid,int)
        pipe.sadd(self.JOB_PID_KEY%{'hostname':self.hostname},pid)




class SlaveStatusRequestManager(SlaveStatusBaseManager):
    jobProcessClass=JobRequestProcess
    JOB_PID_KEY=JOB_REQUEST_PID_KEY

    # 快捷方式
    def get_parallel_job_size(self):
        return slaveInfoManager.get_parallel_job_request_size()

    def get_parallel_job_pids(self):
        return slaveInfoManager.get_parallel_job_request_pids()




class SlaveStatusItemManager(SlaveStatusBaseManager):
    jobProcessClass=JobItemProcess
    JOB_PID_KEY=JOB_ITEM_PID_KEY

     # 快捷方式
    def get_parallel_job_size(self):
        return slaveInfoManager.get_parallel_job_item_size()

    def get_parallel_job_pids(self):
        return slaveInfoManager.get_parallel_job_item_pids()


slaveStatusItemManager=SlaveStatusItemManager()
slaveStatusRequestManager=SlaveStatusRequestManager()