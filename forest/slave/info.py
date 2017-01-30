#coding=utf-8
from ..rd import rd_conn
import config

MAX_PROCESS_REQUEST_COUNT_KEY=config.MAX_PROCESS_REQUEST_COUNT_KEY # 最大单次请求处理数量
MAX_PROCESS_ITEM_COUNT_KEY=config.MAX_PROCESS_ITEM_COUNT_KEY # 最大item 处理数量
DEFAULT_MAX_PROCESS_REQUEST_COUNT=config.DEFAULT_MAX_PROCESS_REQUEST_COUNT # 默认最大请求处数量
DEFAULT_MAX_PROCESS_ITEM_COUNT=config.DEFAULT_MAX_PROCESS_ITEM_COUNT # 默认item 最大处理数量


class SlaveInfo(object):
    """获取slave 的一些信息的实现类"""
    def __init__(self,server):
        self.server=server


    def get_max_process_request_count(self,hostname):
        c=self.server.get(MAX_PROCESS_REQUEST_COUNT_KEY%{"hostname":hostname})
        try:
            return int(c)
        except TypeError:
            return DEFAULT_MAX_PROCESS_REQUEST_COUNT

    def get_max_process_item_count(self,hostname):
        c=self.server.get(MAX_PROCESS_ITEM_COUNT_KEY%{"hostname":hostname})
        try:
            return int(c)
        except TypeError:
            return DEFAULT_MAX_PROCESS_ITEM_COUNT

    def set_max_process_item_count(self,hostname,c):
        assert isinstance(c,int) and c>0

        return self.server.set(MAX_PROCESS_ITEM_COUNT_KEY%{"hostname":hostname},c)


    def set_max_process_request_count(self,hostname,c):
        assert isinstance(c,int) and c>0

        return self.server.set(MAX_PROCESS_REQUEST_COUNT_KEY%{"hostname":hostname},c)


slaveInfo=SlaveInfo(rd_conn)