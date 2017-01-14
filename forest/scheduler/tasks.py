#coding=utf-8
#调度器

# from c import C
from forest.http import RequestBase,ResponseBase
from celery import Celery
from forest.settings.final_settings import default_scheduler_settings_path
C=Celery()
C.config_from_object(default_scheduler_settings_path)
# import sys
# todo 暂时的
# sys.path.append('f:/forest/example/')
# sys.path.append('/mnt/hgfs/project/forest/example/')


@C.task()
def process_request(request,**kwargs):
    spider=request.spider
    callback=request.callback
    for mw in spider.mws:
        request=mw.process_request(request) # request 肯能是一个响应或者请求（出错的时候）
        if not isinstance(request,(RequestBase,ResponseBase)):
            break
    return getattr(spider,callback)(request) # 注意： request 可能是一个响应或者请求（出错的时候）



@C.task()
def process_item(item,**kwargs):
    spider=item.spider
    for pip in spider.pips:
        item=pip.process_item(item) # 处理item 入库

