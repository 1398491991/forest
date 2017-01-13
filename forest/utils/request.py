#coding=utf8

def request_fingerprint(request):
    return True # 暂时的


from misc import pickle_loads,pickle_dumps
from forest.db.rd import rd_conn
from forest.settings.final_settings import *

def request_restore_from_redis(name):
    """根据爬虫名称 返回获取的列表list"""
    try:
        return pickle_loads(rd_conn.lpop(spider_off_collect_request_keys%name))
    except TypeError:
        return None
    # return map(lambda x:pickle_loads(x),rd_conn.lrange(spider_off_collect_request_keys%name,0,-1))



def request_collect_to_redis(name,request):
    """爬虫名称 请求实例"""

    return rd_conn.rpush(spider_off_collect_request_keys%name,pickle_dumps(request))