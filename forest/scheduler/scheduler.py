#coding=utf-8
#调度器

# import sys
# import os

from forest.settings import default_settings
from forest.utils.conver import setting_conver,Setting
from forest.import_api import ManagerMiddleware
import sys
sys.path.append('f:/forest/example/')
import settings # project setting 需要如添加到sys.path
from celery import Celery

# 配置该项目设置
project_settings=setting_conver(default_settings)
project_settings.update(setting_conver(settings)) # 合并配置文件
project_settings=Setting(project_settings)


scheduler_app = Celery(**project_settings.get('scheduler_settings',{'name':__name__}))
# celery = Celery('tasks',backend='redis://10.0.0.12:6379/0', broker='redis://10.0.0.12:6379/0')
manager_middleware=ManagerMiddleware.from_settings(project_settings) # 实例化中间件管理器

from forest.http import Request,FormRequest

@scheduler_app.task
def process_request(request,**kwargs):
    spider=request.spider
    for mw in spider.mws:
        request=mw.process_request(request) # request 肯能是一个响应
    # response=requests.request(**request) # 这里还要详细些
    return getattr(request.spider,request.callback)(request)