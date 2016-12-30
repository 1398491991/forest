# import scrapy
from forest.decorator.async import async_request
from forest.spiders import Spider
from forest.http import Response
a=1
class Demo(Spider):


    @async_request
    def run1(self,a):
        return [{'url':'http://www.baidu.com',
                 'callback':'run2',
                 'self':self},]*10

    def run2(self,response):
        print '#################  ',response





