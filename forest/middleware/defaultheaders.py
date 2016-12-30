#coding=utf-8

class DefaultHeadersMiddleware(object):
    """设置一个默认的请求头部 借鉴scrapy"""
    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):
        # 请求的实例 设置表头
        if not hasattr(request,'headers') or \
                not isinstance(request.headers,dict):
            request.headers=self.settings.get('default_headers',
                                                       {'user-agent':'forest'}
                                                       )
        return request

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)
