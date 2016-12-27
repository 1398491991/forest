# import scrapy
from forest.decorator.spider import delay
from forest.spiders import Spider

class Demo(Spider):


    @delay
    def run1(self):
        return [{'url':'http://www.baidu.com',
                 'callback':'run2',
                 'self':self},]*10

    def run2(self,response):
        print '#################  ',response





