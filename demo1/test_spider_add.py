#coding=utf-8
import sys
sys.path.append('/mnt/hgfs/project/forest/')
sys.path.append('/mnt/hgfs/forest/')
sys.path.append('d:/forest/')

from forest.services.add import AddSpider
from test_spider import testSpider

t=testSpider()
d={'spider_instance':t.to_pickle(),
   'spider_name':t.name,
   'spider_max_url_length':0,
   'spider_min_url_length':0,
   'spider_request_retry_count':3,
   'spider_project_path':['/mnt/hgfs/project/forest/demo1']}

a=AddSpider(d)
a.add()
a.commit(raise_on_error=True)
