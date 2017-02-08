#coding=utf-8
from forest.services.info import getSpiderInfo

class DownLoadTimeOutMiddleware(object):
    """设置默认超时中间件"""


    def get_spider_request_timeout(self,spider_name):
        return getSpiderInfo.get_spider_request_timeout(spider_name)

    def process_request(self,request):
        if not request.timeout:
            request.timeout=self.get_spider_request_timeout(request.from_spider)
        return request


