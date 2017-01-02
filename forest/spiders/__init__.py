# coding=utf-8
# 自己编写  spider 的集合
# from scrapy import Spider

from forest.utils.misc import load_object

class Spider(object):
    """借鉴 scrapy """

    name=None
    config=None
    custom_settings = {}

    custom_middleware={} # 设置一些爬虫私有的的中间件加载路径 优先使用 防止 celery 重启


    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def load_config(self,path):
        """加载爬虫配置文件"""
        self.config=load_object(path)


    def start(self):
        """爬虫的启动方法"""
        pass

    def parse(self,response):
        """默认回调调用的方法"""
        pass


    def load_custom_middleware(self):
        """
        加载定制的中间件 这样方便celery不用重启针对新的爬虫
        :setting dict
        :return None
        """
        from forest.utils.misc import load_project_setting
        self.project_setting=load_project_setting()

        self.mw_list=[]

if __name__ == '__main__':
    s=Spider(1)
    print s.__dict__

