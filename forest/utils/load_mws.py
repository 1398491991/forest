#coding=utf-8
from forest.utils.misc import load_object

class LoadSpiderMiddleware(object):
    """通过爬虫配置文件加载此爬虫相对应的中间件"""
    def __init__(self,spider_config):
        self.spider_config=spider_config
        print self.spider_config
        self.cfg=self.spider_config['middleware'] # 获取配置中间件的字典
        assert self.cfg #不能为空


    def __sort_cfg(self,desc=False):
        rank_key=sorted(self.cfg,cmp=lambda x,y:cmp(self.cfg[x],self.cfg[y]),reverse=desc)
        return rank_key

    def load_mws(self,desc=False):
        # 返回排序的中间件的实例对象
        return [load_object(key)(self.spider_config) for key in self.__sort_cfg(desc)]

