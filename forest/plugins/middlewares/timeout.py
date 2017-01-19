#coding=utf-8
from forest.utils.info import SpiderInfo

class DownLoadTimeOutMiddleware(object):
    """设置默认超时中间件"""
    def __init__(self,settings):
        self.settings=settings
        self.info=SpiderInfo(self.settings['name'])

    def get_timeout(self):
        return self.info.get_spider_download_timeout()

    def process_request(self,request):
        if not request.timeout:
            request.timeout=self.get_timeout()
        return request


    @classmethod
    def from_settings(cls,settings):
        return cls(settings)

