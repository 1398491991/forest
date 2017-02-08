import sys
sys.path.append('/mnt/hgfs/project/forest/')
sys.path.append('/mnt/hgfs/forest/')
sys.path.append('d:/forest/')

from forest.services.add import AddRequest
from forest.http.request import Request

# AddRequest(Request(url='https://123.sogou.com/',priority=10,from_spider='demo2')).add()
AddRequest(Request(url='http://127.0.0.1:5000/123',priority=10,from_spider='demo2')).add()