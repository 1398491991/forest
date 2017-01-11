#coding=utf8

from forest.spiders import Spider
from forest.http import Request
from forest.decorator.async import async
import time


class Demo(Spider):
    start_urls = ['http://10.0.0.12:5000/1']*10

    @async
    def parse(self,response):
        """默认回调调用的方法"""
        print response.url
        print response.xpath('/')
        res=int(response.text)+1
        time.sleep(1)
        return [Request('http://10.0.0.12:5000/%s'%res,callback='parse1')]

    @async
    def parse1(self,response):
        print response.url
        print response.xpath('/')
        time.sleep(1)
        res=int(response.text)+1
        return [Request('http://10.0.0.12:5000/%s'%res,callback='parse')]




