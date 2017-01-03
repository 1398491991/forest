# coding=utf-8
# 自己编写  spider 的集合
# from scrapy import Spider

from forest.utils.misc import load_object
from forest.utils.misc import obj_to_dict
from forest.utils.xpython import Dict
from forest.utils.load_mws import LoadSpiderMiddleware

class Spider(object):
    """借鉴 scrapy """

    def __init__(self,config,default_config):
        self.config=Dict(default_config)
        self.config.update(Dict(config)) # 合并配置


    @classmethod
    def config_from_py(cls,config_path,default_config_path=None):
        """通过配置文件加载"""
        config,default_config=map(lambda x:obj_to_dict(load_object(x)),[config_path,
                                                                        default_config_path or 'forest.settings.default_settings'])
        return cls(config,default_config)


    def load_down_mws(self,desc=False):
        """加载下载中间件实例列表 是否降序排序"""
        self.mws=LoadSpiderMiddleware(self.config).load_mws(desc)

    def start(self):
        """爬虫的启动方法"""
        pass

    def parse(self,response):
        """默认回调调用的方法"""
        pass


if __name__ == '__main__':
    s=Spider({},{})
    print s.__dict__

