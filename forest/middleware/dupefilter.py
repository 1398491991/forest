#coding=utf-8
import requests
from forest.http import Response
from forest.utils.select import Selector

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
            return self.__bind(response,request)

    def __bind(self,response,request):
        """绑定对象到响应"""
        response.request=request
        if request.encoding:
            response.encoding=request.encoding
        select=Selector(response.text,base_url=response.url)
        return Response(response,select)

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)