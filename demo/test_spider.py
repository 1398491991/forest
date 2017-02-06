
from forest.spider import Spider
from forest.async import async
from forest.http.request import Request
from forest.utils.misc import get_host_name

host_name=get_host_name()
class testSpider(Spider):
    name='test'

    @async
    def parse(self,response):
        # try:
        #     url=int(response.url.split('/')[-1])+1
        # except Exception as e:
        #     print e
        #     url=1
        # url=
        # return [Request(url='http://127.0.0.1:5000/%s'%url),]
        return [#Request(url='http://127.0.0.1:5000/%s'%url),
            #Request(url='http://127.0.0.1:5000/5555'),
                Request(url='http://127.0.0.1:5000/123',appoint_name=host_name,priority=10)]*2