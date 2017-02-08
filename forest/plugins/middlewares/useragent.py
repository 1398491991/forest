#coding=utf-8
from forest.services.info import getSpiderInfo

class UserAgentMiddleware(object):


    def get_spider_request_user_agent(self,spider_name):
        return getSpiderInfo.get_spider_request_user_agent(spider_name)

    def process_request(self, request):
        request.headers.setdefault('User-Agent', self.get_spider_request_user_agent(
            request.from_spider
        ))
        return request
