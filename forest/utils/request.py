#coding=utf8

def request_fingerprint(request):
    return True # 暂时的


from misc import pickle_loads,pickle_dumps
from forest.db.rd import rd_conn
from forest.settings.final_settings import *

def request_restore_from_redis(name):
    """根据爬虫名称 返回获取的列表list"""
    return map(lambda x:pickle_loads(x),rd_conn.lrange(spider_off_collect_request_keys%name,0,-1))



def request_collect_to_redis(name,request):
    """爬虫名称 请求实例"""
    request=pickle_dumps(request)
    return rd_conn.rpush(name,request)