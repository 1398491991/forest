# import scrapy
from forest.decorator.async import async
from forest.spiders import Spider
from forest.http import Request

class Demo(Spider):

    @async
    def run1(self,response=None):
        return (Request(url='http://10.0.0.12:8000/admin/login/?next=/admin/',callback='run2'),)*10

    @async
    def run2(self,response):
        # print '#################  ',response.text
        return (Request(url='http://10.0.0.12:8000/admin/login/?next=/admin/',callback='run1',),)*10




