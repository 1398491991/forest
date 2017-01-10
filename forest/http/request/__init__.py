#coding=utf-8
# from scrapy import Request

import json
from requests import Request as rq_Request

class RequestBase(rq_Request):
    """ 参考第三方模块 requests 参数没变"""
    base_attrs=['method','url','params','data',
        'headers','cookies','files','auth','timeout',
        'allow_redirects','proxies','hooks',
        'stream','verify','cert','json']
    attrs=base_attrs

    def __init__(self,url, method,spider=None,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None):

        super(RequestBase,self).__init__(method, url, headers, files,
        data, params, auth, cookies, hooks, json)
        self.spider=spider
        self.timeout=timeout
        self.allow_redirects=allow_redirects
        self.proxies=proxies
        self.verify=verify
        self.cert=cert
        self.stream=stream

    def to_json(self):

        return json.dumps(self.to_dict())

    def to_dict(self):
        return {k:getattr(self,k) for k in self.attrs}


    def safe_attr(self,attr,attr_type):

        if self.exist_attr(attr):
            return isinstance(getattr(self,attr),attr_type)
        return False

    def exist_attr(self,attr):
        return hasattr(self,attr)

    def __getitem__(self, item):
        if isinstance(item,basestring):
            return getattr(self,item)
        return map(lambda x:getattr(self,x),item)

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__


class Request(RequestBase):
    """添加优先级等参数，参考scrapy request 定义"""
    attr = RequestBase.attrs+['callback','priority','encoding',
                                              'errorback','meta']

    def __init__(self,url,**kwargs):
        self.spider=kwargs.pop('spider',None)
        self.callback=kwargs.pop('callback','parse')
        self.priority=kwargs.pop('priority',0)
        self.encoding=kwargs.pop('encoding',None)
        self.dont_filter=kwargs.pop('dont_filter',False)
        self.errorback=kwargs.pop('errorback',None)
        self.meta = kwargs.pop('meta',{})
        assert isinstance(self.meta,dict)
        super(Request,self).__init__(url,kwargs.pop('method','GET'),**kwargs)



class FormRequest(Request):
    def __init__(self,url,**kwargs):
        if 'method' not in kwargs:
            kwargs['method']='POST'
        super(FormRequest,self).__init__(url,**kwargs)
        assert self.method=='POST'



if __name__ == '__main__':
    a=Request(2222,callback='run2',spider=123)
    print a
    print a.to_dict()['method']
    print a.to_json()
