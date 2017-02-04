#coding=utf-8
import sys
sys.path.append('/mnt/hgfs/forest/')
sys.path.append('d:/forest/')
from forest.spider.info import SpiderInfo
from forest.spider.add import AddSpider
from forest.utils.serializable import dump_pickle
from test_spider import testSpider

t=testSpider()
d={'spider_instance':t.to_pickle(),
   'spider_name':t.name,
   'spider_max_url_length':0,
   'spider_min_url_length':0,
   'spider_retry_count':3,
   'spider_project_path':['d:/demo']}

a=AddSpider(d)
a.add()
a.commit(raise_on_error=True)
