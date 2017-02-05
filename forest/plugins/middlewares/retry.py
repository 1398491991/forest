#coding=utf-8
from forest.spider.info import spiderInfo

class RetryMiddleware(object):


    def get_spider_request_retry_count(self,spider_name):
        """获取最大重试次数"""
        return spiderInfo.get_spider_request_retry_count(spider_name)


    def process_request(self,request):
        # 是否超过最大重试次数
        if not hasattr(request,'retry_count'):
            request.retry_count=0
            return request
        # log
        request.retry_count+=1
        retry_max_count=self.get_spider_request_retry_count(request.from_spider)
        if request.retry_count>retry_max_count:
            return None
        return request
