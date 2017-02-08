import sys
sys.path.append('/mnt/hgfs/project/forest/')
sys.path.append('/mnt/hgfs/forest/')
sys.path.append('d:/forest/')
# from test_spider import testSpider
# test=testSpider()
# from forest.http.response import Response
# test.parse(Response(1,2))

from forest.services.add import AddRequest
from forest.http.request import Request

# AddRequest(Request(url='https://123.sogou.com/',priority=10,from_spider='test')).add()
AddRequest(Request(url='http://127.0.0.1:5000/123',from_spider='test')).add()