#coding=utf-8
from forest.spider.info import getSpiderInfo

class MaxLengthMiddleware(object):


    def get_spider_max_url_length(self,spider_name):
        return getSpiderInfo.get_spider_max_url_length(spider_name)

    def process_request(self, request):
        max_length=self.get_spider_max_url_length(request.from_spider)
        if not max_length or len(request.url)<=max_length:
            return request



class MinLengthMiddleware(object):

    def get_spider_min_url_length(self,spider_name):
        return getSpiderInfo.get_spider_min_url_length(spider_name)

    def process_request(self, request):
        min_length=self.get_spider_min_url_length(request.from_spider)
        if not min_length or len(request.url)>=min_length:
            return request

