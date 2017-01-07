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

class Spider(object):
    """借鉴 scrapy """
    name='forest' # example

    def __init__(self,config):
        self.config=Dict(config)
        assert self.name # 不能为空

    @classmethod
    def config_from_py(cls,config_path,default_config_path=None):
        """通过配置文件加载"""
        default_config=obj_to_dict(load_object(default_config_path or 'forest.settings.default_settings'))
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
        urls=rd_conn.smembers('forest:spider:%s_init_urls'%self.name)
        if not urls:
            import warnings
            warnings.warn('spider <%s> start urls is Null'%self.name)
        return map(lambda url:Request(url),urls)



    @async
    def parse(self,response):
        """默认回调调用的方法"""
        raise NotImplementedError
