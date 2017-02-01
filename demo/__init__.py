
from test_spider import testSpider
test=testSpider()
from forest.http.response import Response
test.parse(Response(1,2))
# from forest.manager.spider_instance import spiderInstanceManager
# spiderInstanceManager.set_spider_instance(test)

# print test.to_pickle()
# from forest.http.response import Response
# test.parse(123)