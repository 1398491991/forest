# coding=utf-8
"""
移除 spider 各项指标的方法集合
"""
from info import RemoveSpiderInfo


class RemoveSpider(object):
    removeSpiderInfo=RemoveSpiderInfo(transaction=True)

    def __init__(self,spider_name):
        self.removeSpiderInfo.spider_name=spider_name

    def remove(self):

        self.removeSpiderInfo.rm_spider_name()
        self.removeSpiderInfo.rm_spider_instance()
        self.removeSpiderInfo.rm_spider_max_url_length()
        self.removeSpiderInfo.rm_spider_min_url_length()
        self.removeSpiderInfo.rm_spider_project_path()
        self.removeSpiderInfo.rm_spider_request_retry_count()
        self.removeSpiderInfo.rm_spider_request_headers()
        self.removeSpiderInfo.rm_spider_request_timeout()
        self.removeSpiderInfo.rm_spider_request_user_agent()


    def commit(self, raise_on_error=True):
        self.removeSpiderInfo.execute(raise_on_error)