#coding=utf-8
"""
将requests 的返回响应 进行包装  扩展功能
"""
from requests import Response as rq_Response
from ..response import Response

class ResponseExt(object):
    """待实现"""

    def ext(self,rq_response):
        assert isinstance(rq_response,rq_Response)


    def bind_css(self):
        pass

    def bind_xpath(self):
        pass

    def __init__(self,rq_response):
        assert isinstance(rq_response,rq_Response)
        self.rq_response=rq_response

        self.response=Response()

    def parse_attr(self):
        attrs=rq_Response.__attrs__

        for attr in  attrs:
            setattr(self.response,attr,getattr(self.response,attr))


