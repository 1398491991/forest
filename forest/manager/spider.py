#coding=utf-8
"""添加一个新的 spider 到 redis 中 """
from ..rd import rd_conn
import config

RETRY_COUNT=config.RETRY_COUNT
URL_MAX_LENGTH=config.URL_MAX_LENGTH
URL_MIN_LENGTH=config.URL_MIN_LENGTH
SPIDER_INSTANCE_KEY=config.SPIDER_INSTANCE_KEY

class AddSpider(object):
    def __init__(self,
                 spider_instance_pickle,
                 spider_name,
                 project_path,
                 retry_count=RETRY_COUNT,
                 url_max_length=URL_MAX_LENGTH,
                 url_min_length=URL_MIN_LENGTH,
                 cookies=None,
                 bad_urls=None,
                 start_urls=None,
                 ):
        assert isinstance(spider_instance_pickle,basestring)
        self.spider_instance_pickle=spider_instance_pickle

        assert spider_name
        self.spider_name=spider_name
        self.project_path=project_path
        self.retry_count=retry_count
        self.url_max_length=url_max_length
        self.url_min_length=url_min_length
        self.cookies=cookies or {}
        self.bad_urls=bad_urls or []
        self.start_urls=start_urls or []

        self.spider_instance_key=SPIDER_INSTANCE_KEY%{'spider_name':spider_name}


    @property
    def rd_conn(self):
        return rd_conn

    def add(self):
        pipe = self.rd_conn.pipeline() # 事务处理


    def exists_spider(self):
        return self.rd_conn.exists(self.spider_instance_key)