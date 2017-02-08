
from forest.spider.plain import PlainSpider
from forest.async import async
from forest.http.request import Request


class testSpider(PlainSpider):
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
                Request(url='http://127.0.0.1:5000/123')]*10
        # return task_route.delay(Request(url='http://127.0.0.1:5000/123',priority=10))