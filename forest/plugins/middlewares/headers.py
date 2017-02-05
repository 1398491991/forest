#coding=utf-8
from forest.rd import rd_conn
import config

SPIDER_REQUEST_HEADERS_KEY=config.SPIDER_REQUEST_HEADERS_KEY  # HSET
DEFAULT_SPIDER_REQUEST_HEADERS =config.DEFAULT_SPIDER_REQUEST_HEADERS

class HeadersMiddleware(object):
    """设置一个默认的请求头部 借鉴scrapy"""


    def get_spider_request_headers(self,spider_name):
        res=rd_conn.hgetall(SPIDER_REQUEST_HEADERS_KEY % {'spider_name':spider_name})
        return res or DEFAULT_SPIDER_REQUEST_HEADERS

    def process_request(self,request):
        # 请求的实例 设置表头
        if not request.headers:# 没有设置头
            request.headers=self.get_spider_request_headers(request.from_spider)
        return request