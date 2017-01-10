#coding=utf-8

class UserAgentMiddleware(object):
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, settings):
        self.settings = settings

    def get_user_agent(self):
        return self.settings['user_agent']

    def process_request(self, request):
        request.headers.setdefault('User-Agent', self.get_user_agent())
        return request
