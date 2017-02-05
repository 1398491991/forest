#coding=utf-8

from forest.spider.info import spiderInfo



class HeadersMiddleware(object):
    """设置一个默认的请求头部 借鉴scrapy"""


    def get_spider_request_headers(self,spider_name):
        return spiderInfo.get_spider_request_headers(spider_name)


    def process_request(self,request):
        # 请求的实例 设置表头
        if not request.headers:# 没有设置头
            request.headers=self.get_spider_request_headers(request.from_spider)
        return request