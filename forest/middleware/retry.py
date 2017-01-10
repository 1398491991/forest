#coding=utf-8
from forest.http import RequestBase
from forest.decorator.plugin import filter_type

class RetryMiddleware(object):
    def __init__(self,settings):
        self.settings=settings

    def get_retry_max_count(self):
        """获取最大重试次数"""
        return self.settings.getint['retry_max_count']

    @filter_type(RequestBase)
    def process_request(self,request):
        # 是否超过最大重试次数

        if request.retry_count>self.get_retry_max_count():
            return None
        return request
