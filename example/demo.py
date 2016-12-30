# import scrapy
from forest.decorator.async import async_request
from forest.spiders import Spider
from forest.http import Request
a=1
class Demo(Spider):


    @async_request
    def run1(self):
        # (Request(url='http://www.baidu.com',callback='run2',),)*10
        return (Request(url='http://10.0.0.12:8000/admin/login/?next=/admin/',callback='run2',spider=self),)*10

    def run2(self,response):
        print '#################  ',response.text
        # return (Request(url='http://$$$$$$$$$$$$$$$$$$$$idu.com',callback='run2',spider=self),)*10#




