#coding=utf-8

class DefaultHeadersMiddleware(object):

    @staticmethod
    def process_request(request):
        if not getattr(request,'headers'):
            request.headers={'user-agent':'forest'}
        return request
