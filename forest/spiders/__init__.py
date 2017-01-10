# coding=utf-8
# 自己编写  spider 的集合
# from scrapy import Spider

from forest.utils.misc import load_object
from forest.utils.misc import obj_to_dict
from forest.utils.xpython import Dict
from forest.utils.load import LoadSpiderMiddleware,LoadSpiderPipeline
from forest.db.rd import rd_conn
from forest.decorator.async import async
from forest.http import Request
from forest.http import ResponseBase
from forest.settings.final_settings import *

class Spider(object):
    """借鉴 scrapy """
    name='forest' # example
    start_urls=[]



    def __init__(self,config):
        self.config=Dict(config)
        assert self.name # 不能为空

        self.start_urls_key=spider_start_urls_keys%self.name

    @classmethod
    def config_from_py(cls,config_path):
        """通过配置文件加载"""
        default_config=obj_to_dict(load_object(default_spider_settings_path))
        config=obj_to_dict(load_object(config_path)) if config_path else {}

        default_config.update(config) # 合并配置
        return cls(default_config)


    def load_ext(self):
        """加载下载中间件实例列表 是否降序排序"""
        self.mws=LoadSpiderMiddleware(self.config).load()
        self.pips=LoadSpiderPipeline(self.config).load()

    def start(self):
        """爬虫的启动方法"""
        self.load_ext() # 加载中间件和管道
        return self.make_init_request(ResponseBase())

    @async
    def make_init_request(self,response):
        """初始的请求来自于redis"""
        t=rd_conn.type(self.start_urls_key)
        f=rd_conn.rpush if t=='list' else rd_conn.sadd
        urls=f(self.start_urls_key)
        if urls:
            return map(lambda url:Request(url),urls)

        import warnings
        warnings.warn('spider <%s> start urls is Null'%self.name)



    def start_urls_to_redis(self,allow_same=False):
        """将初始Url放入 redis """

        f=rd_conn.rpush if allow_same else rd_conn.sadd
        for url in self.start_urls:
            f(self.start_urls_key,url)
        # rd_conn.llen()


    @async
    def parse(self,response):
        """默认回调调用的方法"""
        raise NotImplementedError
