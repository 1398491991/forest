# import scrapy
from forest.decorator.async import async
from forest.spiders import Spider
from forest.http import Request
import time

class Demo(Spider):

    @async
    def run1(self,response):
        print response
        return (Request(url='http://10.0.0.12:8000/admin/login/?next=/admin/',callback='run2'),)*5

    @async
    def run2(self,response):
        # time.sleep(2)
        print '#################  ',response
        # return (Request(url='http://10.0.0.12:8000/admin/login/?next=/admin/',callback='run1',),)




