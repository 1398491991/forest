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

    def get_spider_instance(self,spider_name,to_obj=True,
                            local_copy=True):
        def to_obj_func(spider_instance):
            if isinstance(spider_instance,basestring):
                return load_pickle(spider_instance)
            return spider_instance

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
            if to_obj:
                spider_instance=to_obj_func(spider_instance)
            if local_copy:
                setattr(self,attr,to_obj_func(spider_instance))

            return spider_instance

        except ImportError:
            raise SpiderImportError,spider_name


spiderInstanceManager=SpiderInstanceManager()