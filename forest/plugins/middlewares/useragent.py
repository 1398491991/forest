#coding=utf-8
from forest.utils.info import SpiderInfo

class UserAgentMiddleware(object):


    def __init__(self, settings):
        self.settings = settings
        self.info=SpiderInfo(self.settings['name'])

    def get_user_agent(self):
        return self.info.get_spider_unique_user_agent()

    def process_request(self, request):
        request.headers.setdefault('User-Agent', self.get_user_agent())
        return request
