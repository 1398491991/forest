#coding=utf-8
#调度器
from forest.settings import default_settings
from forest.utils.to_map import setting_to_map,Map
from forest.import_api import Request
from forest.import_api import ManagerMiddleware
#### example
import sys
sys.path.append('f:/forest/example/')
import settings
####
from celery import Celery

celery = Celery('tasks',backend='redis://10.0.0.12:6379/0', broker='redis://10.0.0.12:6379/0')

default_settings_map=Map(setting_to_map(default_settings))
settings_map=Map(setting_to_map(settings))
settings_map.update(default_settings_map) # 合并配置文件
manager_middleware=ManagerMiddleware(settings) # 实例化中间件管理器
# from example.demo import test
# t=test()
import requests
# import redis
# rq=redis.Redis('10.0.0.12')
print sys.path


@celery.task
def process_request(request,**kwargs):
    # assert isinstance(request,dict)
    # request=Request(**request)
    # todo : do something...
    print request
    # import pickle
    # return request
    # return requests.get(request['url'])
    # print rq.get('test')
    res=requests.get(request['url'])
    # t=getattr(request['self'](),request['callback'])
    return getattr(request['self'],request['callback'])(res)
    # return manager_middleware.process(request)