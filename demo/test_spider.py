
from forest.spider import Spider
from forest.async import async
from forest.http.request import SimpleRequest


class testSpider(Spider):
    name='test'

    @async
    def parse(self,response):
        return SimpleRequest(url='http://127.0.0.1:5000/123',method='get')


