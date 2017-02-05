#coding=utf-8


class DupeFilterMiddleware(object):

    """过滤请求"""
    def process_request(self,request):
        return request
