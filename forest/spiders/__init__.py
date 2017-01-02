# coding=utf-8
# 自己编写  spider 的集合
# from scrapy import Spider

from forest.utils.misc import load_object
from forest.utils.misc import obj_to_dict
from forest.utils.xpython import Dict
from forest.utils.load_mws import LoadSpiderMiddleware

class Spider(object):
    """借鉴 scrapy """

    def __init__(self,config):
        self.config=config


    @classmethod
    def config_from_py(cls,path):
        """通过配置文件加载"""
        cfg=Dict(obj_to_dict(load_object(path)))
        return cls(cfg)



    def load_down_mws(self):
        """加载下载中间件"""
        self.mws=LoadSpiderMiddleware(self.config)

    def start(self):
        """爬虫的启动方法"""
        pass

    def parse(self,response):
        """默认回调调用的方法"""
        pass


if __name__ == '__main__':
    s=Spider(1)
    print s.__dict__

