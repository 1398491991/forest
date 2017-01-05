#coding=utf-8
import redis

class RdConn(object):
    def __init__(self,*args,**kwargs):
        self.rd_conn=redis.Redis(*args,**kwargs)

    def config_from_object(self,path):
        pass

