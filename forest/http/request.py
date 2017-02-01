#coding=utf8
import requests
from ..utils.serializable import dump_json

class Request(requests.Request):
    def __init__(self,url,method=None, headers=None, files=None,
        data=None, params=None, auth=None, cookies=None, hooks=None, json=None,
                 # ext
                 from_spider=None,project_path=None,callback='parse',
                 priority=0,appoint_name=None,meta=None,
                 # replace
                 replace_optional=None):
        super(Request,self).__init__(method, url, headers, files,
        data, params, auth, cookies, hooks, json)

        self.from_spider=from_spider
        assert isinstance(priority,int)
        self.priority=priority
        self.meta=meta or {}
        self.appoint_name=appoint_name
        self.callback=callback
        self.project_path=project_path or []
        self.replace_optional=replace_optional or {}

    def to_json(self):
        return dump_json(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return '<Request [%s] [%s]>' % (self.method,self.url)

    __str__=__repr__