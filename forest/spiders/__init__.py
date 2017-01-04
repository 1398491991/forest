# coding=utf-8
# 自己编写  spider 的集合
# from scrapy import Spider

from forest.utils.misc import load_object
from forest.utils.misc import obj_to_dict
from forest.utils.xpython import Dict
from forest.utils.load_mws import LoadSpiderMiddleware

class Spider(object):
    """借鉴 scrapy """
    name=''

    def __init__(self,config):
        self.config=Dict(config)

    @classmethod
    def config_from_py(cls,config_path,default_config_path=None):
        """通过配置文件加载"""
        default_config=obj_to_dict(load_object(default_config_path or 'forest.settings.default_settings'))
        config=obj_to_dict(load_object(config_path)) if config_path else {}
        default_config.update(config) # 合并配置
        return cls(default_config)


    def load_down_mws(self,desc=False):
        """加载下载中间件实例列表 是否降序排序"""
        self.mws=LoadSpiderMiddleware(self.config).load_mws(desc)

    def start(self):
        """爬虫的启动方法"""
        self.load_down_mws()

    def parse(self,response):
        """默认回调调用的方法"""
        pass


if __name__ == '__main__':
    s=Spider({})
    print s.__dict__

