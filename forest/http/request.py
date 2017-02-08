#coding=utf8
import requests
from ..utils.serializable import dump_json

class Request(requests.Request):
    def __init__(self,url,method='GET', headers=None, files=None,
        data=None, params=None, auth=None, cookies=None, hooks=None, json=None,
                 timeout=None,allow_redirects=None,proxies=None,
                 verify=None,stream=False,cert=None,
                 # ext
                 **kwargs):
        super(Request,self).__init__(method, url, headers, files,
        data, params, auth, cookies, hooks, json)

        self.timeout=timeout
        self.allow_redirects=allow_redirects
        self.proxies=proxies
        self.verify=verify
        self.stream=stream
        self.cert=cert

        self.from_spider=kwargs.pop('from_spider', None)
        self.priority=kwargs.pop('priority', 0)
        assert isinstance(self.priority, int)
        self.encoding=kwargs.pop('encoding','utf-8')
        self.meta=kwargs.pop('meta', {})
        self.callback=kwargs.pop('callback', 'parse')
        self.replace_optional=kwargs.pop('replace_optional', {})
        self.async_optional=kwargs.pop('async_optional', {})



    def to_json(self):
        return dump_json(self.to_dict())

    def to_dict(self):
        return self.__dict__

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def __repr__(self):
        return '<Request [%s] [%s]>' % (self.method,self.url)

    __str__=__repr__