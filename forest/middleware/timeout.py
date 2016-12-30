#coding=utf-8

class DownLoadTimeOutMiddleware(object):
    """下载超时中间件"""

    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):
        pass

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)



class DefaultTimeOutMiddleware(object):
    """设置默认超时中间件"""
    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):
        if not request.safe_attr('timeout',(int,float)):
            request.timeout=self.settings['timeout']
        return request

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)

