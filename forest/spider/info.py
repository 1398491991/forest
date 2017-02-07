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





class BaseSpiderInfo(object):

    def __init__(self,spider_name=None,transaction=False):
        """当 spider_name =None  那么使用 get 方法类似静态使用"""
        self._spider_name = spider_name

        self._transaction= transaction

        self.rd_server=rd_conn.pipeline() if self.transaction else rd_conn

    @property
    def key_format(self):
        assert self._spider_name
        return {'spider_name':self._spider_name}

    @property
    def spider_name(self):
        return self._spider_name

    @spider_name.setter
    def spider_name(self,spider_name):

        self._spider_name=spider_name


    def execute(self,raise_on_error=True):
        if self._transaction:
            return self.rd_server.execute(raise_on_error)

    @property
    def transaction(self):
        return self._transaction

    @transaction.setter
    def transaction(self,transaction):
        self.rd_server=rd_conn.pipeline() if transaction else rd_conn
        self._transaction=transaction





class SetSpiderInfo(BaseSpiderInfo):

    def set_spider_name(self,name,ignore_exist=False):
        """添加爬虫名称"""
        # 单独设置
        if name in rd_conn.smembers(SPIDER_NAME_KEY) and not ignore_exist:
            raise SpiderNameExistError,name
        return self.rd_server.sadd(SPIDER_NAME_KEY,name) # transaction exe

    def exist_key(self,key,ignore_exist):
        if rd_conn.exists(key) and not ignore_exist:
            raise KeyExistError,key

    def set_spider_instance(self,spider, ignore_exist=False):
        assert isinstance(spider,basestring) # pickle
        key = SPIDER_INSTANCE_KEY%self.key_format
        self.exist_key(key,ignore_exist)
        return self.rd_server.set(key, spider)


    def set_spider_request_retry_count(self,retry_count, ignore_exist=False):
        retry_count=retry_count or DEFAULT_SPIDER_RETRY_COUNT
        assert isinstance(retry_count, int) and retry_count > 0
        key = SPIDER_RETRY_COUNT_KEY%self.key_format
        self.exist_key(key,ignore_exist)
        return self.rd_server.set(key, retry_count)


    def set_spider_max_url_length(self,length, ignore_exist=False):
        # 0 表示没有限制
        if length is None:
            length = DEFAULT_SPIDER_URL_MAX_LENGTH
        assert isinstance(length,int) and length >=0
        return self.rd_server.set(SPIDER_URL_MAX_LENGTH_KEY % self.key_format, length)



    def set_spider_min_url_length(self,length, ignore_exist=False):
        # 0 表示没有限制
        if length is None:
            length = DEFAULT_SPIDER_URL_MIN_LENGTH
        assert isinstance(length,int) and length >=0
        return self.rd_server.set(SPIDER_URL_MIN_LENGTH_KEY % self.key_format, length)


    def set_spider_project_path(self,path, ignore_exist=False):
        assert isinstance(path,(tuple,list,set)) and path
        key=SPIDER_PROJECT_PATH_KEY%self.key_format
        self.exist_key(key,ignore_exist)
        return self.rd_server.sadd(key,*path)


    def set_spider_request_headers(self,headers, ignore_exist=False):
        headers=headers or DEFAULT_SPIDER_REQUEST_HEADERS
        assert isinstance(headers,dict)
        self.rd_server.hmset(SPIDER_REQUEST_HEADERS_KEY % self.key_format ,headers)



    def set_spider_request_timeout(self,timeout, ignore_exist=False):
        timeout=timeout or DEFAULT_SPIDER_REQUEST_TIMEOUT
        assert isinstance(timeout,(int,float)) and timeout>0
        return self.rd_server.set(
                         SPIDER_REQUEST_TIMEOUT_KEY % self.key_format,
                         timeout,)


    def set_spider_request_user_agent(self,user_agent, ignore_exist=False):
        user_agent=user_agent or [DEFAULT_SPIDER_REQUEST_USER_AGENT,]
        assert isinstance(user_agent,(list,tuple,set))
        return self.rd_server.sadd(
                         SPIDER_REQUEST_USER_AGENT_KEY % self.key_format,
                         user_agent,)




class GetSpiderInfo(BaseSpiderInfo):


    def get_spider_instance(self,spider_name=None):
        """为了不需要多次初始化一个变量 设置成类似 静态方法的调用"""

        return self.rd_server.get(SPIDER_INSTANCE_KEY%{'spider_name':spider_name or self.spider_name})


    def get_spider_max_url_length(self,spider_name=None):
        try:
            return self.rd_server.get(SPIDER_URL_MAX_LENGTH_KEY%{'spider_name':spider_name or self.spider_name})
        except TypeError:
            return DEFAULT_SPIDER_URL_MAX_LENGTH

    def get_spider_min_url_length(self,spider_name=None):
        try:
            return self.rd_server.get(SPIDER_URL_MIN_LENGTH_KEY%{'spider_name':spider_name or self.spider_name})
        except TypeError:
            return DEFAULT_SPIDER_URL_MIN_LENGTH

    def get_spider_project_path(self,spider_name=None):
        return self.rd_server.smembers(SPIDER_PROJECT_PATH_KEY%{'spider_name':spider_name or self.spider_name})

    def get_spider_request_retry_count(self,spider_name=None):
        res=self.rd_server.get(SPIDER_RETRY_COUNT_KEY%{'spider_name':spider_name or self.spider_name})
        try:
            return int(res)
        except TypeError:
            return DEFAULT_SPIDER_RETRY_COUNT

    def get_spider_request_headers(self,spider_name=None):
        res=self.rd_server.hgetall(SPIDER_REQUEST_HEADERS_KEY %{'spider_name':spider_name or self.spider_name})
        return res or DEFAULT_SPIDER_REQUEST_HEADERS


    def get_spider_request_timeout(self,spider_name=None):
        try:
            return float(self.rd_server.get(SPIDER_REQUEST_TIMEOUT_KEY%{'spider_name':spider_name or self.spider_name}))
        except TypeError:
            return DEFAULT_SPIDER_REQUEST_TIMEOUT

    def get_spider_request_user_agent(self,spider_name=None):

        res=self.rd_server.srandmember(SPIDER_REQUEST_USER_AGENT_KEY%{'spider_name':spider_name or self.spider_name})
        if not res:
            res=DEFAULT_SPIDER_REQUEST_USER_AGENT
        return res


class RemoveSpiderInfo(BaseSpiderInfo):


    def delete_key(self,*key):
        return self.rd_server.delete(*key)

    def rm_spider_name(self,spider_name=None):
        """为了不需要多次初始化一个变量 设置成类似 静态方法的调用"""
        return self.rd_server.srem(SPIDER_NAME_KEY ,spider_name or self.spider_name)



    def rm_spider_instance(self,spider_name=None):
        """为了不需要多次初始化一个变量 设置成类似 静态方法的调用"""
        return self.delete_key(SPIDER_INSTANCE_KEY%{'spider_name':spider_name or self.spider_name})


    def rm_spider_max_url_length(self,spider_name=None):

        return self.delete_key(SPIDER_URL_MAX_LENGTH_KEY%{'spider_name':spider_name or self.spider_name})


    def rm_spider_min_url_length(self,spider_name=None):

        return self.delete_key(SPIDER_URL_MIN_LENGTH_KEY%{'spider_name':spider_name or self.spider_name})


    def rm_spider_project_path(self,spider_name=None):

        return self.delete_key(SPIDER_PROJECT_PATH_KEY%{'spider_name':spider_name or self.spider_name})

    def rm_spider_request_retry_count(self,spider_name=None):

        return self.delete_key(SPIDER_RETRY_COUNT_KEY%{'spider_name':spider_name or self.spider_name})


    def rm_spider_request_headers(self,spider_name=None):

        return self.delete_key(SPIDER_REQUEST_HEADERS_KEY %{'spider_name':spider_name or self.spider_name})


    def rm_spider_request_timeout(self,spider_name=None):

        return self.delete_key(SPIDER_REQUEST_TIMEOUT_KEY%{'spider_name':spider_name or self.spider_name})


    def rm_spider_request_user_agent(self,spider_name=None):

        return self.delete_key(SPIDER_REQUEST_USER_AGENT_KEY%{'spider_name':spider_name or self.spider_name})


# setSpiderInfo=SetSpiderInfo(transaction=True)
getSpiderInfo=GetSpiderInfo(transaction=False)
# removeSpiderInfo=RemoveSpiderInfo(transaction=True)