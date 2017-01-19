#coding=utf-8
from forest.utils.info import SpiderInfo

class HeadersMiddleware(object):
    """设置一个默认的请求头部 借鉴scrapy"""
    def __init__(self,settings):
        self.settings=settings
        self.info=SpiderInfo(self.settings['name'])

    def get_default_headers(self):
        return self.info.get_unique_spider_header()


    def process_request(self,request):
        # 请求的实例 设置表头
        if not request.headers:# 没有设置头
            request.headers=self.get_default_headers()
        return request

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)
