#coding=utf-8
from forest.db.rd import rd_conn
from forest.settings.final_settings import spider_name_keys,spider_project_path_keys
import os
from forest.utils.exceptions import RegisterSpiderException,ProjectPathNotExistsException


class RegisterSpider(object):
    """注册一个爬虫"""
    def __init__(self,spider):
        self.spider=spider
        assert isinstance(self.spider.project_path,(list,tuple))
        self.project_path_keys=spider_project_path_keys%self.spider.name # 爬虫项目储存键值

    def register_spider_name(self):
        """注册名称成功为 True 否则 False"""
        try:
            return bool(rd_conn.sadd(spider_name_keys,self.spider.name))
        except Exception as e:
            raise RegisterSpiderException,e

    def register_project_path(self):
        """注册项目路径 一个爬虫允许多个路径（多台机器） 但是本地一定有"""
        res=False
        for path in self.spider.project_path:
            if  os.path.exists(path):
                res=True
                break
        if not res:
            raise ProjectPathNotExistsException,self.spider.project_path
        try:
            # 不允许重复 所以用集合
            rd_conn.sadd(self.project_path_keys,self.spider.project_path)
            return True
        except Exception as e:
            raise RegisterSpiderException,e


    def register(self):
        if self.register_spider_name():
            # 注册成功名称
            if self.register_project_path():
                # 注册路径成功
                return True
            # 路径注册失败 删除爬虫名称
            rd_conn.srem(spider_name_keys,self.spider.name)

        return False

        # 否则 爬虫名称注册失败
