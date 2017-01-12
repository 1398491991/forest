#coding=utf-8
"""从redis中获取spider一些信息的api"""
from forest.db.rd import rd_conn
import warnings
from forest.settings.final_settings import *


def get_spider_status(name):
    """根据爬虫名称 返回当前设置状态"""
    res=rd_conn.get(spider_status_keys%name)
    print res,'$$$$$$$$$$$$$$$$$$$$'
    if not res:
        # 爬虫不存在
        warnings.warn('spider <%s> not exist'%name)
    return res

def get_spider_collect_status(name):
    """根据爬虫名称获取 是否同步请求"""
    res=rd_conn.get(spider_off_collect_request_status_keys%name)
    if not res:
        # 爬虫不存在
        warnings.warn('spider <%s> not exist'%name)
        res=1 # 默认同步 防止 出错
    return bool(int(res))

def update_spider_status(name,status):
    """更新爬虫的状态"""
    assert status in ('on','off')
    return rd_conn.set(spider_status_keys%name,status)