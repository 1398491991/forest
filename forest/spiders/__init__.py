# coding=utf-8
# 自己编写  spider 的集合
# from scrapy import Spider

from forest.utils.misc import load_object
from forest.utils.misc import obj_to_dict
from forest.utils.xpython import Dict
from forest.utils.load_mws import LoadSpiderMiddleware

class Spider(object):
    """借鉴 scrapy """

    def __init__(self,config,
                 default_config_path=None):
        self.config=Dict(config)
        self.merge_config(self.load_default_config(default_config_path)) # 更新默认配置文件

    @classmethod
    def config_from_py(cls,path):
        """通过配置文件加载"""
        cfg=obj_to_dict(load_object(path))
        return cls(cfg)


    def load_default_config(self,path=None):
        default_config=load_object(path or 'forest.settings.default_settings')
        return default_config

    def merge_config(self,default_config):
        """合并配置"""
        self.config.update(default_config)

    def load_down_mws(self,desc=False):
        """加载下载中间件"""
        self.mws=LoadSpiderMiddleware(self.config).load_mws(desc)

    def start(self):
        """爬虫的启动方法"""
        pass

    def parse(self,response):
        """默认回调调用的方法"""
        pass


if __name__ == '__main__':
    s=Spider(1)
    print s.__dict__

