# coding=utf-8
from ..rd import rd_conn
import config


SPIDER_NAME_KEY=config.SPIDER_NAME_KEY
SPIDER_INSTANCE_KEY=config.SPIDER_INSTANCE_KEY
SPIDER_PROJECT_PATH_KEY=config.SPIDER_PROJECT_PATH_KEY
SPIDER_URL_MAX_LENGTH_KEY=config.SPIDER_URL_MAX_LENGTH_KEY
SPIDER_URL_MIN_LENGTH_KEY=config.SPIDER_URL_MIN_LENGTH_KEY
SPIDER_RETRY_COUNT_KEY=config.SPIDER_RETRY_COUNT_KEY
SPIDER_REQUEST_TIMEOUT_KEY=config.SPIDER_REQUEST_TIMEOUT_KEY
SPIDER_REQUEST_USER_AGENT_KEY=config.SPIDER_REQUEST_USER_AGENT_KEY


DEFAULT_SPIDER_URL_MAX_LENGTH=config.DEFAULT_SPIDER_URL_MAX_LENGTH # 0 表示没有限制
DEFAULT_SPIDER_URL_MIN_LENGTH=config.DEFAULT_SPIDER_URL_MIN_LENGTH # 0 表示没有限制
DEFAULT_SPIDER_RETRY_COUNT=config.DEFAULT_SPIDER_RETRY_COUNT
DEFAULT_SPIDER_REQUEST_TIMEOUT=config.DEFAULT_SPIDER_REQUEST_TIMEOUT
DEFAULT_SPIDER_REQUEST_USER_AGENT=config.DEFAULT_SPIDER_REQUEST_USER_AGENT

SPIDER_REQUEST_HEADERS_KEY=config.SPIDER_REQUEST_HEADERS_KEY  # HSET
DEFAULT_SPIDER_REQUEST_HEADERS =config.DEFAULT_SPIDER_REQUEST_HEADERS


class KeyExistError(Exception):
    def __init__(self,key):
        self.key=key

    def __repr__(self):
        return '<key "%s" exist>'%self.key

    __str__ = __repr__

class SpiderInstanceExistError(Exception):
    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<spider "%s" instance exist>'%self.name

    __str__=__repr__

class SpiderNameExistError(Exception):
    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return '<spider "%s" name exist>'%self.name

    __str__=__repr__



def key_exist(key, raise_error=True, **kwargs):
    assert isinstance(raise_error, bool)
    res = rd_conn.exists(key)
    if res and raise_error:
        raise KeyExistError,key
    return res


def _key_exist_decorator(raise_error=True):
    """适用于下面 spiderinfo 类"""
    def _func(func):

        def _decorator_func(self,f, key,*args, **kwargs):
            # if 'ignore_error' in kwargs
            __raise_error=kwargs.pop('raise_error',None)
            _raise_error=raise_error
            if __raise_error is not None:
                _raise_error=__raise_error
            key_exist(key,_raise_error,**kwargs)
            func(self,f,key,*args, **kwargs)

        return _decorator_func

    return _func




class SpiderInfo(object):
    """获取 和 设置 spider 信息"""

    def __repr__(self):
        return '<%s> SpiderInfo'%self.spider_name

    __str__=__repr__

    def __init__(self, spider_name):
        """当 spider_name =None  那么使用get 方法类似静态使用"""
        self.spider_name = spider_name
        self.rd_pipe=rd_conn.pipeline()
        self.rd_conn=rd_conn
        self.spider_name_map={'spider_name':self.spider_name}

    def set_spider_name(self,name,raise_error=True,**kwargs):
        """添加爬虫名称"""
        # 单独设置
        if name in self.rd_conn.smembers(SPIDER_NAME_KEY) and raise_error:
            raise SpiderNameExistError,name
        return self.rd_pipe.sadd(SPIDER_NAME_KEY,name)


    def set_spider_instance(self,spider,**kwargs):
        assert isinstance(spider,basestring) # pickle
        return self._set(self.rd_pipe.set,SPIDER_INSTANCE_KEY%self.spider_name_map,
                         spider,** kwargs)



    def set_spider_request_retry_count(self,retry_count,**kwargs):
        retry_count=retry_count or DEFAULT_SPIDER_RETRY_COUNT
        assert isinstance(retry_count, int) and retry_count > 0
        return self._set(self.rd_pipe.set,
                         SPIDER_RETRY_COUNT_KEY%self.spider_name_map,
                         retry_count,** kwargs)



    def set_spider_max_url_length(self,length,**kwargs):
        # 0 表示没有限制
        if length is None:
            length = DEFAULT_SPIDER_URL_MAX_LENGTH
        assert isinstance(length,int) and length >=0
        return self._set(self.rd_pipe.set,
                         SPIDER_URL_MAX_LENGTH_KEY%self.spider_name_map,
                         length,** kwargs)


    def set_spider_min_url_length(self,length,**kwargs):
        # 0 表示没有限制
        if length is None:
            length = DEFAULT_SPIDER_URL_MIN_LENGTH
        assert isinstance(length, int) and length >=0
        return self._set(self.rd_pipe.set,
                         SPIDER_URL_MIN_LENGTH_KEY % self.spider_name_map,
                         length,** kwargs)


    def set_spider_project_path(self,path,raise_error=True):
        assert isinstance(path,(tuple,list,set))
        key=SPIDER_PROJECT_PATH_KEY%self.spider_name_map
        key_exist(key,raise_error)
        return self.rd_pipe.sadd(key,*path)


    def set_spider_request_headers(self,headers,**kwargs):
        headers=headers or DEFAULT_SPIDER_REQUEST_HEADERS
        assert isinstance(headers,dict)
        return self._set(self.rd_pipe.hmset,
                         SPIDER_REQUEST_HEADERS_KEY % self.spider_name_map,
                         headers, **kwargs)


    def set_spider_request_timeout(self,timeout,**kwargs):
        timeout=timeout or DEFAULT_SPIDER_REQUEST_TIMEOUT
        assert isinstance(timeout,(int,float)) and timeout>0
        return self._set(self.rd_pipe.set,
                         SPIDER_REQUEST_TIMEOUT_KEY % self.spider_name_map,
                         timeout, **kwargs)


    def set_spider_request_user_agent(self,user_agent,**kwargs):
        user_agent=user_agent or [DEFAULT_SPIDER_REQUEST_USER_AGENT,]
        assert isinstance(user_agent,(list,tuple,set))
        return self._set(self.rd_pipe.sadd,
                         SPIDER_REQUEST_USER_AGENT_KEY % self.spider_name_map,
                         user_agent, **kwargs)



    @_key_exist_decorator(True)
    def _set(self,method,key,value,**kwargs):
        # kwargs 也有 raise_error 参数 覆盖 _key_exist_decorator 参数
        return method(key,value) if not isinstance(value,(list,tuple,set)) else method(key,*value)

    def execute(self,raise_on_error=True):
        """只针对 set 方法"""
        self.rd_pipe.execute(raise_on_error)

############################ 以上set方法主要用于更新爬虫设置信息 ############################


    def get_spider_instance(self,spider_name=None):
        """为了不需要多次初始化一个变量 设置成类似 静态方法的调用"""

        return self.rd_conn.get(SPIDER_INSTANCE_KEY%{'spider_name':spider_name or self.spider_name})


    def get_spider_max_url_length(self,spider_name=None):
        try:
            return self.rd_conn.get(SPIDER_URL_MAX_LENGTH_KEY%{'spider_name':spider_name or self.spider_name})
        except TypeError:
            return DEFAULT_SPIDER_URL_MAX_LENGTH

    def get_spider_min_url_length(self,spider_name=None):
        try:
            return self.rd_conn.get(SPIDER_URL_MIN_LENGTH_KEY%{'spider_name':spider_name or self.spider_name})
        except TypeError:
            return DEFAULT_SPIDER_URL_MIN_LENGTH

    def get_spider_project_path(self,spider_name=None):
        return self.rd_conn.smembers(SPIDER_PROJECT_PATH_KEY%{'spider_name':spider_name or self.spider_name})

    def get_spider_request_retry_count(self,spider_name=None):
        res=self.rd_conn.get(SPIDER_RETRY_COUNT_KEY%{'spider_name':spider_name or self.spider_name})
        try:
            return int(res)
        except TypeError:
            return DEFAULT_SPIDER_RETRY_COUNT

    def get_spider_request_headers(self,spider_name=None):
        res=self.rd_conn.hgetall(SPIDER_REQUEST_HEADERS_KEY %{'spider_name':spider_name or self.spider_name})
        return res or DEFAULT_SPIDER_REQUEST_HEADERS


    def get_spider_request_timeout(self,spider_name=None):
        try:
            return float(self.rd_conn.get(SPIDER_REQUEST_TIMEOUT_KEY%{'spider_name':spider_name or self.spider_name}))
        except TypeError:
            return DEFAULT_SPIDER_REQUEST_TIMEOUT

    def get_spider_request_user_agent(self,spider_name=None):

        res=self.rd_conn.srandmember(SPIDER_REQUEST_USER_AGENT_KEY%{'spider_name':spider_name or self.spider_name})
        if not res:
            res=DEFAULT_SPIDER_REQUEST_USER_AGENT
        return res


    def rm(self):
        pass


spiderInfo=SpiderInfo(None) # 方便 get method 使用