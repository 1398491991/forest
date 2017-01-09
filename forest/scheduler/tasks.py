#coding=utf-8
#调度器
import sys
from c import C
sys.path.append('f:/forest/example/')
sys.path.append('/mnt/hgfs/project/forest/example/')

@C.task()
def process_request(request,**kwargs):
    spider=request.spider
    callback=request.callback
    for mw in spider.mws:
        request=mw.process_request(request) # request 肯能是一个响应或者请求（出错的时候）
    return getattr(spider,callback)(request) # 注意： request 可能是一个响应或者请求（出错的时候）



@C.task()
def process_item(item,**kwargs):
    spider=item.spider
    for pip in spider.pips:
        item=pip.process_item(item) # 处理item 入库
