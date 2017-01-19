#coding=utf8
from forest.utils.misc import load_object
from ..async import async

class SimpleSpider(object):
    name=''

    def __init__(self):
        assert self.name

    @async
    def parse(self,response):
        raise NotImplementedError

    def load_plugins(self,mws_path_sort_list,pipes_path_sort_list):
        """加载插件  顺序很重要"""
        self.mws=map(lambda x:load_object(x)(),mws_path_sort_list)
        self.pipes=map(lambda x:load_object(x)(),pipes_path_sort_list)

    def __repr__(self):
        return '<Spider [%s]>' % (self.name)

    __str__=__repr__

Spider=SimpleSpider