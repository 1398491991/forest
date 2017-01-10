#coding=utf-8


class HttpProxyMiddleware(object):

    def __init__(self,settings):
        self.settings=settings

    def process_request(self, request):
        return request

