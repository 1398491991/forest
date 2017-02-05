#coding=utf8
from ..utils.serializable import load_pickle,dump_pickle
from ..rd import rd_conn
from ..spider.info import SpiderInfo
# import config
import sys

# SPIDER_INSTANCE_KEY=config.SPIDER_INSTANCE_KEY

class SpiderImportError(Exception):
    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<spider "%s" import error>'%self.name

class SpiderInstanceExistError(Exception):
    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<spider "%s" instance exist>'%self.name


class SpiderInstanceManager(object):
    """管理spider 实例"""
    @property
    def rd_conn(self):
        return rd_conn

    def get_spider_instance(self,spider_name,):

        attr='spider_%s'%spider_name
        if hasattr(self,attr):
            return getattr(self,attr)
        try:
            info=SpiderInfo(spider_name)
            # project_path=info.get_spider_project_path()
            # sys.path.extend(project_path)
            spider_instance=info.get_spider_instance()

            # key=SPIDER_INSTANCE_KEY%{'spider_name':spider_name}
            # spider_instance=self.rd_conn.get(key)
            spider_instance=load_pickle(spider_instance)
            setattr(self,attr,spider_instance)

            return spider_instance

        except ImportError:
            raise SpiderImportError,spider_name


spiderInstanceManager=SpiderInstanceManager()