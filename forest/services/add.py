#coding=utf-8
from forest.http.request import Request
from forest.utils.serializable import load_json,load_pickle
from forest.async import async
from forest.services.info import SetSpiderInfo
import sys


class AddSpider(object):
    """利用一个json 或者 dict 的相关信息 注册添加一个新的爬虫 有些字段经过pickle序列化 """

    setSpiderInfo=SetSpiderInfo(transaction=True)

    def __init__(self,json_or_dict):
        if isinstance(json_or_dict,basestring):
            json_or_dict=load_json(json_or_dict)
        self.d=json_or_dict

        self.setSpiderInfo.spider_name=self.spider_name
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
        return self.d.get('spider_max_url_length')

    @property
    def spider_min_url_length(self):
        return self.d.get('spider_min_url_length')

    @property
    def spider_request_retry_count(self):
        return self.d.get('spider_request_retry_count')

    @property
    def spider_request_headers(self):
        return self.d.get('spider_request_headers')

    @property
    def spider_request_timeout(self):
        return self.d.get('spider_request_timeout')

    @property
    def spider_request_user_agent(self):
        return self.d.get('spider_request_user_agent')

    @property
    def spider_request_cookies_status(self):
        return self.d.get('spider_request_cookies_status','allow')

    @property
    def spider_request_cookies(self):
        return self.d.get('spider_request_cookies')

    def add(self):
        self.setSpiderInfo.set_spider_name(self.spider_name)
        self.setSpiderInfo.set_spider_instance(self.spider_instance)
        self.setSpiderInfo.set_spider_request_headers(self.spider_request_headers)
        self.setSpiderInfo.set_spider_request_timeout(self.spider_request_timeout)
        self.setSpiderInfo.set_spider_request_user_agent(self.spider_request_user_agent)
        self.setSpiderInfo.set_spider_project_path(self.spider_project_path)
        self.setSpiderInfo.set_spider_max_url_length(self.spider_max_url_length)
        self.setSpiderInfo.set_spider_min_url_length(self.spider_min_url_length)
        self.setSpiderInfo.set_spider_request_retry_count(self.spider_request_retry_count)
        self.setSpiderInfo.set_spider_request_cookies_status(self.spider_request_cookies_status)
        self.setSpiderInfo.set_spider_request_cookies(self.spider_request_cookies)

    def test_load(self):
        """测试是否能够正确反序列化"""
        sys.path = list(set(sys.path+list(self.spider_project_path)))
        return load_pickle(self.spider_instance)

    def commit(self,raise_on_error=True):
        return self.setSpiderInfo.execute(raise_on_error)





class AddRequest(object):

    def __init__(self,request):
        self.request= request

    @classmethod
    def from_json(cls,request_json):
        return cls(Request(**load_json(request_json)))


    @classmethod
    def from_dict(cls,request_dict):
        return cls(Request(**request_dict))

    @classmethod
    def from_pickle(cls,request_pickle):
        return cls(Request(**load_pickle(request_pickle)))

    def add(self):
        return async.apply_async(self.request)


