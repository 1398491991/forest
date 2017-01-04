#coding=utf-8
#调度器
import sys
sys.path.append('f:/forest/example/')
# sys.path.append('f:/forest/forest/')
# print sys.path
from celery import Celery
# scheduler_app = Celery(**project_settings.get('scheduler_settings',{'name':__name__}))
scheduler_app = Celery('tasks', broker='redis://10.0.0.12:6379/0')
# scheduler_app = Celery('tasks',backend='redis://10.0.0.12:6379/0', broker='redis://10.0.0.12:6379/0')


@scheduler_app.task
def process_request(request,**kwargs):
    spider=request.spider
    d_mw=spider.mws[-1]
    for mw in spider.mws[:-1]:
        request=mw.process_request(request) # request 肯能是一个响应或者请求（出错的时候）
    response=d_mw.process_request(request)
    # response=requests.request(**request) # 这里还要详细些
    # print request,'$$$$$$$$$$$$$$$$$$'
    return getattr(spider,request.callback)(response)