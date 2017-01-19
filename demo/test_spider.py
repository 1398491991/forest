
from forest.spider import Spider

class testSpider(Spider):
    name='test'

    def parse(self,response):
        print 'hahahh'
