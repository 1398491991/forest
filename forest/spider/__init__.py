#coding=utf8
from forest.utils.misc import load_object
from forest.utils.serializable import dump_pickle
from ..async import async

class Spider(object):
    name=''
    rules=[]
    mws_path_sort_list=['forest.plugins.middlewares.dupefilter.DupeFilterMiddleware',
                        'forest.plugins.middlewares.retry.RetryMiddleware',
                        'forest.plugins.middlewares.headers.HeadersMiddleware',
                        'forest.plugins.middlewares.useragent.UserAgentMiddleware',
                        'forest.plugins.middlewares.httpproxy.HttpProxyMiddleware',
                        'forest.plugins.middlewares.timeout.DownLoadTimeOutMiddleware',
                        ]

    pipes_path_sort_list=[]
    # 加载插件  顺序很重要

    def __init__(self):
        assert self.name
        self.load_plugins()

    @async
    def parse(self,response):
        raise NotImplementedError

    def load_plugins(self):
        """加载插件  顺序很重要"""
        self.mws=map(lambda x:load_object(x)(),self.mws_path_sort_list)
        self.pipes=map(lambda x:load_object(x)(),self.pipes_path_sort_list)

    def to_pickle(self):
        return dump_pickle(self)

    def __repr__(self):
        return '<Spider [%s]>' % (self.name)

    __str__=__repr__
