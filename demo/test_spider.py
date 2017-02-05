
from forest.spider import Spider
from forest.async import async
from forest.http.request import Request
from forest.utils.misc import get_host_name

host_name=get_host_name()
class testSpider(Spider):
    name='test'

    @async
    def parse(self,response):
        return [Request(url='http://127.0.0.1:5000/123'),
                Request(url='http://127.0.0.1:5000/123',appoint_name=host_name,priority=10)]*2