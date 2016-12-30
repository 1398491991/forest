#coding=utf-8
import requests


class DownLoadMiddleware(object):

    """下载中间件  直接使用 requests 模块"""
    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):

        return self.__curl(request)

    def __curl(self,request):
        try:
            response=requests.request(**{x:getattr(request,x) for x in request.base_attrs})
        except:
            return request
        else:
            return response

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)