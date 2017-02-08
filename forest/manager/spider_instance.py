#coding=utf8
from ..utils.serializable import load_pickle
from ..rd import rd_conn
from forest.services.info import getSpiderInfo
import sys



class SpiderImportError(Exception):
    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<spider "%s" import error>'%self.name




class SpiderInstanceManager(object):
    """管理spider 实例"""
    getSpiderInfo=getSpiderInfo

    @property
    def rd_conn(self):
        return rd_conn

    def get_spider_instance(self,spider_name,):

        attr='spider_%s'%spider_name
        if hasattr(self,attr):
            return getattr(self,attr)
        try:
            project_path=self.getSpiderInfo.get_spider_project_path(spider_name)
            sys.path=list(set(sys.path+list(project_path)))
            spider_instance=self.getSpiderInfo.get_spider_instance(spider_name)
            spider_instance=load_pickle(spider_instance)
            setattr(self,attr,spider_instance)

            return spider_instance

        except ImportError:
            raise SpiderImportError(spider_name)


spiderInstanceManager=SpiderInstanceManager()