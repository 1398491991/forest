#coding=utf-8
from ..rd import rd_conn
import config

MAX_PROCESS_REQUEST_COUNT_KEY=config.MAX_PROCESS_REQUEST_COUNT_KEY
MAX_PROCESS_ITEM_COUNT_KEY=config.MAX_PROCESS_ITEM_COUNT_KEY
DEFAULT_MAX_PROCESS_REQUEST_COUNT=config.DEFAULT_MAX_PROCESS_REQUEST_COUNT
DEFAULT_MAX_PROCESS_ITEM_COUNT=config.DEFAULT_MAX_PROCESS_ITEM_COUNT


class SlaveInfo(object):
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
        return self.server.set(MAX_PROCESS_ITEM_COUNT_KEY%{"hostname":hostname},c)


    def set_max_process_request_count(self,hostname,c):
        return self.server.set(MAX_PROCESS_REQUEST_COUNT_KEY%{"hostname":hostname},c)


slaveInfo=SlaveInfo(rd_conn)