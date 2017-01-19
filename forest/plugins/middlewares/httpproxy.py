#coding=utf-8

from forest.utils.info import SpiderInfo
class HttpProxyMiddleware(object):

    def __init__(self,settings):
        self.settings=settings
        self.info=SpiderInfo(self.settings['name'])

    def process_request(self, request):
        return request

