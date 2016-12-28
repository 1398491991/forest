#coding=utf-8
import requests

class DownLoadMiddleware(object):
    """下载中间件  直接使用 requests 模块"""
    def __init__(self,settings):
        self.settings=settings

    def process_request(self,request):
        assert isinstance(request,dict)
        response=requests.request(**request)
        return request

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)