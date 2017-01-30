#coding=utf8
from ..utils.parse_config import parseConfig
import os,sys

sys.path.append(os.path.dirname(parseConfig.config_path))
from ..utils.serializable import load_pickle,dump_pickle
from ..rd import rd_conn
import config

SPIDER_INSTANCE_KEY=config.SPIDER_INSTANCE_KEY

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
            key=SPIDER_INSTANCE_KEY%{'spider_name':spider_name}
            spider_instance=rd_conn.get(key)
            if to_obj:
                spider_instance=to_obj_func(spider_instance)
            if local_copy:
                setattr(self,attr,to_obj_func(spider_instance))

            return spider_instance

        except ImportError:
            raise SpiderImportError,spider_name

    def set_spider_instance(self,spider_instance,spider_name=None,
                            to_pickle=False):
        """将 spider 设置到 redis 中"""

        if not isinstance(spider_instance,basestring):
            spider_name=spider_instance.name
            to_pickle=True

        assert spider_name

        key=SPIDER_INSTANCE_KEY%{'spider_name':spider_name}
        if rd_conn.exists(key):
            raise SpiderInstanceExistError,spider_name

        if to_pickle:
            spider_instance=dump_pickle(spider_instance)
        return rd_conn.set(key,spider_instance)


spiderInstanceManager=SpiderInstanceManager()