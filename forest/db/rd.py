#coding=utf-8
import redis
rd_conn=redis.Redis('10.0.0.12') #
# class RdConn(object):
#     def __init__(self,*args,**kwargs):
#         # self.rd_conn=redis.Redis(*args,**kwargs)
#         self.rd_conn=redis.Redis('10.0.0.12') #
#
#     @classmethod
#     def config_from_object(cls,path):
#         pass