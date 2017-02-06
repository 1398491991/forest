import sys
sys.path.append('/mnt/hgfs/project/forest/')
sys.path.append('d:/forest/')
from test_spider import testSpider
test=testSpider()
# from forest.http.request import Request
# a=Request(url='http://127.0.0.1:5000/123',method='get')
# print a.to_dict()
from forest.http.response import Response
test.parse(Response(1,2))
# from forest.manager.spider_instance import spiderInstanceManager
# spiderInstanceManager.set_spider_instance(test)

# print test.to_pickle()
# from forest.http.response import Response
# test.parse(123)