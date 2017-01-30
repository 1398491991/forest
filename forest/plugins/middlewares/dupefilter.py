#coding=utf-8


class DupeFilterMiddleware(object):

    """过滤请求"""
    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):
        if request.dont_filter:
            return request

        bool=request_fingerprint(request)
        if bool:
            return request




    @classmethod
    def from_settings(cls,settings):
        return cls(settings)