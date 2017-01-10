#coding=utf-8


class DefaultHeadersMiddleware(object):
    """设置一个默认的请求头部 借鉴scrapy"""
    def __init__(self,settings):
        self.settings=settings

    def get_default_header(self):
        return self.settings['default_request_header']


    def process_request(self,request):
        # 请求的实例 设置表头
        if not request.headers:# 没有设置头
            request.headers=self.get_default_header()
        return request

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)
