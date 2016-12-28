#coding=utf-8

class DefaultHeadersMiddleware(object):
    """设置一个默认的请求头部 借鉴scrapy"""
    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):
        # assert isinstance(request,dict)
        request.setdefault('headers',self.settings.get('default_headers',
                                                       {'user-agent':'forest'}
                                                       )
                           )
        return request

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)
