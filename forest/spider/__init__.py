#coding=utf8
from forest.utils.misc import load_object
from forest.utils.serializable import dump_pickle
from ..async import async

class Spider(object):
    name=''
    rules=[]

    info={"spider_name":"demo",
        "project_path":[],
        "retry_count":3,
        "url_max_length":None,
        "url_min_length":None,
        "cookies":{},
        "bad_urls":[],
        }

    def __init__(self):
        assert self.name
        assert self.info

    @async
    def parse(self,response):
        raise NotImplementedError

    def load_plugins(self,mws_path_sort_list,pipes_path_sort_list):
        """加载插件  顺序很重要"""
        self.mws=map(lambda x:load_object(x)(),mws_path_sort_list)
        self.pipes=map(lambda x:load_object(x)(),pipes_path_sort_list)

    def spider_to_pickle(self):
        return dump_pickle(self)

    def __repr__(self):
        return '<Spider [%s]>' % (self.name)

    __str__=__repr__
