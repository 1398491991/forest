#coding=utf-8
from six.moves.urllib.parse import urljoin
import six


class Response(object):

    def __init__(self,response,select):
        self.response=response
        self.select=select

    def urljoin(self, url):
        """参考scrapy"""
        return urljoin(self.response.url, url)

    def xpath(self,query):

        return self.select.xpath(query)

    def css(self,query):

        return self.select.css(query)

    def re(self,regex):

        return self.select.re(regex)

    def __getattribute__(self, item):
        if hasattr(self, item):
            return getattr(self,item)

        try:
            return getattr(self.response,item)
        except AttributeError:
            return getattr(self.select,item)


    def __getitem__(self, item):
        if isinstance(item,six.string_types):
            return self.__getattr__(item)

        return map(self.__getattr__,item)


    def __str__(self):
        return "<%s %s>" % (self.response.status_code, self.response.url)

    __repr__ = __str__






