#coding=utf-8
from forest.utils.misc import load_object

class Middleware(object):
    """通过配置文件加载相对应的中间件"""
    def __init__(self,spider_config):
        self.spider_config=spider_config
        self.cfg=self.spider_config['middleware'] # 获取配置中间件的字典

    def sort_cfg(self,desc=False):
        rank_key=sorted(self.cfg,cmp=lambda x,y:cmp(self.cfg[x],self.cfg[y]),reverse=desc)
        return rank_key

    def set_rank_cfg(self):
        rank_key=self.sort_cfg()
        self.rank_cfg=[(key,self.cfg[key]) for key in rank_key]

    def load_mws(self):
        # 返回排序的中间件的实例
        return [load_object(path)(self.spider_config) for key,path in self.rank_cfg]

