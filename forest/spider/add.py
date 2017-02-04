# coding=utf-8
"""
添加 spider 各项指标的方法集合
"""
from ..utils.serializable import load_json,load_pickle
from info import SpiderInfo
import sys

class AddSpider(object):
    """利用一个json 或者 dict 的相关信息 注册添加一个新的爬虫 有些字段经过pickle序列化 """
    def __init__(self,json_or_dict):
        if isinstance(json_or_dict,basestring):
            json_or_dict=load_json(json_or_dict)
        self.d=json_or_dict

        self.spider_info=SpiderInfo(spider_name=self.spider_name)

        self.test_load()

    @property
    def spider_name(self):
        return self.d['spider_name']

    @property
    def spider_instance(self):
        return self.d['spider_instance']

    @property
    def spider_project_path(self):
        return self.d['spider_project_path']


    @property
    def spider_max_url_length(self):
        return self.d['spider_max_url_length']

    @property
    def spider_min_url_length(self):
        return self.d['spider_min_url_length']

    @property
    def spider_retry_count(self):
        return self.d['spider_retry_count']

    def add(self):
        self.spider_info.set_spider_name(self.spider_name)
        self.spider_info.set_spider_instance(self.spider_instance)
        self.spider_info.set_spider_project_path(self.spider_project_path)
        self.spider_info.set_spider_max_url_length(self.spider_max_url_length)
        self.spider_info.set_spider_min_url_length(self.spider_min_url_length)
        self.spider_info.set_spider_retry_count(self.spider_retry_count)

    def test_load(self):
        """测试是否能够正确反序列化"""
        sys.path.extend(list(self.spider_project_path))
        return load_pickle(self.spider_instance)

    def commit(self,raise_on_error=True):
        return self.spider_info.execute(raise_on_error)

