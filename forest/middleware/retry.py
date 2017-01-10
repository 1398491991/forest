#coding=utf-8

class RetryMiddleware(object):
    def __init__(self,settings):
        self.settings=settings

    def get_retry_max_count(self):
        """获取最大重试次数"""
        return self.settings['retry_max_count']


    def process_request(self,request):
        # 是否超过最大重试次数
        if not hasattr(request,'retry_count'):
            request.retry_count=0
            return request

        if request.retry_count>self.get_retry_max_count():
            return None
        return request
