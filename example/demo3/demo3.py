#coding=utf8
# import scrapy
# from forest.decorator.async import async
from forest.spiders import Spider
from forest.http import Request
from forest.decorator.async import async
# from forest.http import Request


class Demo(Spider):
    @async
    def parse(self,response):
        """默认回调调用的方法"""
        print response,'##################'
        # return 1231
        return [Request('http://10.0.0.12:8000/admin/login/?next=/admin/',callback='parse1')]

    @async
    def parse1(self,response):
        return [Request('http://10.0.0.12:8000/admin/login/?next=/admin/',callback='parse')]




