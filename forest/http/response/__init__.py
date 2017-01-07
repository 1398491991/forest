#coding=utf-8
from requests import Response as rq_Response
# from scrapy import http
from six.moves.urllib.parse import urljoin

class ResponseBase(rq_Response):
    pass


class ResponseExt(object):
    pass


class Response(ResponseBase,ResponseExt):

    def decode(self,encode):
        return self.content.decode(encode)

    def xpath(self,x):
        pass

    def css(self,c):
        pass

    def re(self,r):
        pass

    def urljoin(self, url):
        """参考scrapy"""
        return urljoin(self.url, url)



