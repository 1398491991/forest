#coding=utf-8
#调度器
import sys
from forest.decorator.misc import update_sys_path
# sys.path.append('f:/forest/example/')
# sys.path.append('f:/forest/forest/')
# print sys.path
# assert 'f:/forest/example/' not in sys.path
import kombu
import pickle
from kombu.serialization import BytesIO, register


# def loads(s):
#     print '????????????????????'
#     if 'd:/forest/example/' not in sys.path:
#         print '\n*****************************\n'
#         sys.path.append('d:/forest/example/')
#     return pickle.load(BytesIO(s))
#
# register('pickle', pickle.dumps, loads,
#         content_type='application/x-pickle2',
#         content_encoding='binary')


from celery import Celery
# scheduler_app = Celery(**project_settings.get('scheduler_settings',{'name':__name__}))
import billiard
import kombu
# scheduler_app = Celery('tasks', broker='redis://localhost:6379/0')
scheduler_app = Celery('tasks', broker='redis://10.0.0.12:6379/0')
# scheduler_app = MyCelery('tasks', broker='redis://10.0.0.12:6379/0')
# scheduler_app = Celery('tasks',backend='redis://10.0.0.12:6379/0', broker='redis://10.0.0.12:6379/0')

# if 'd:/forest/example/' not in sys.path:
#     print '\n*****************************\n'
sys.path.append('f:/forest/example/')

@scheduler_app.task()
def process_request(request,**kwargs):
    spider=request.spider
    callback=request.callback
    for mw in spider.mws:
        request=mw.process_request(request) # request 肯能是一个响应或者请求（出错的时候）
    return getattr(spider,callback)(request) # 注意： request 可能是一个响应或者请求（出错的时候）



@scheduler_app.task()
def process_item(item,**kwargs):
    spider=item.spider
    for pip in spider.pips:
        item=pip.process_item(item) # 处理item 入库

