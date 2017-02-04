# coding=utf-8
from ..rd import rd_conn
import config
# import redis
# rd_conn=redis.Redis()


SPIDER_NAME_KEY=config.SPIDER_NAME_KEY
SPIDER_INSTANCE_KEY=config.SPIDER_INSTANCE_KEY
SPIDER_PROJECT_PATH_KEY=config.SPIDER_PROJECT_PATH_KEY
SPIDER_URL_MAX_LENGTH_KEY=config.SPIDER_URL_MAX_LENGTH_KEY
SPIDER_URL_MIN_LENGTH_KEY=config.SPIDER_URL_MIN_LENGTH_KEY
SPIDER_RETRY_COUNT_KEY=config.SPIDER_RETRY_COUNT_KEY

DEFAULT_SPIDER_URL_MAX_LENGTH=config.DEFAULT_SPIDER_URL_MAX_LENGTH # 0 表示没有限制
DEFAULT_SPIDER_URL_MIN_LENGTH=config.DEFAULT_SPIDER_URL_MIN_LENGTH # 0 表示没有限制
DEFAULT_SPIDER_RETRY_COUNT=config.DEFAULT_SPIDER_RETRY_COUNT

def key_exist(key, raise_error=True, ):
    assert isinstance(raise_error, bool)
    res = rd_conn.exists(key)
    if res and raise_error:
        raise Exception, 'exist key %s' % key
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
            key_exist(key,_raise_error)
            return func(self,f,key,*args, **kwargs)

        return _decorator_func

    return _func



class SpiderInfo(object):
    """获取 和 设置 spider 信息"""



    def __init__(self, spider_name):
        self.spider_name = spider_name
        self.rd_pipe=rd_conn.pipeline()
        self.rd_conn=rd_conn
        self.spider_name_map={'spider_name':self.spider_name}

    def set_spider_name(self,name,raise_error=True,**kwargs):
        """添加爬虫名称"""
        # 单独设置
        if name in self.rd_conn.smembers(SPIDER_NAME_KEY) and raise_error:
            raise Exception,'spider name <%s> exist'%name
        return self.rd_pipe.sadd(SPIDER_NAME_KEY,name)


    def set_spider_instance(self,spider,**kwargs):
        assert isinstance(spider,basestring)
        return self._set(self.rd_pipe.set,SPIDER_INSTANCE_KEY%self.spider_name_map,
                         spider,** kwargs)



    def set_spider_retry_count(self,retry_count,**kwargs):
        assert isinstance(retry_count, int) and retry_count > 0
        return self._set(self.rd_pipe.set,
                         SPIDER_RETRY_COUNT_KEY%self.spider_name_map,
                         retry_count,** kwargs)



    def set_spider_max_url_length(self,length,**kwargs):
        # 0 表示没有限制
        assert isinstance(length,int) and length >=0
        return self._set(self.rd_pipe.set,
                         SPIDER_URL_MAX_LENGTH_KEY%self.spider_name_map,
                         length,** kwargs)


    def set_spider_min_url_length(self,length,**kwargs):
        # 0 表示没有限制
        assert isinstance(length, int) and length >=0
        return self._set(self.rd_pipe.set,
                         SPIDER_URL_MIN_LENGTH_KEY % self.spider_name_map,
                         length,** kwargs)


    def set_spider_project_path(self,path,raise_error=True):
        assert isinstance(path,(tuple,list))
        key=SPIDER_PROJECT_PATH_KEY%self.spider_name_map
        key_exist(key,raise_error)
        return self.rd_pipe.sadd(key,*path)


    @_key_exist_decorator(True)
    def _set(self,method,key,value,**kwargs):
        # kwargs 也有 raise_error 参数 覆盖 _key_exist_decorator 参数
        return method(key,value)

    def execute(self,raise_on_error=True):
        """只针对 set 方法"""
        self.rd_pipe.execute(raise_on_error)



    def get_spider_instance(self):
        return self.rd_conn.get(SPIDER_INSTANCE_KEY%self.spider_name_map
                                )

    def get_spider_retry_count(self):
        res=self.rd_conn.get(SPIDER_RETRY_COUNT_KEY%self.spider_name_map)
        try:
            return int(res)
        except TypeError:
            return DEFAULT_SPIDER_RETRY_COUNT

    def get_spider_max_url_length(self):
        try:
            return self.rd_conn.get(SPIDER_URL_MAX_LENGTH_KEY%self.spider_name_map)
        except TypeError:
            return DEFAULT_SPIDER_URL_MAX_LENGTH

    def get_spider_min_url_length(self,length):
        try:
            return self.rd_conn.get(SPIDER_URL_MIN_LENGTH_KEY%self.spider_name_map)
        except TypeError:
            return DEFAULT_SPIDER_URL_MIN_LENGTH

    def get_spider_project_path(self):
        return self.rd_conn.smembers(SPIDER_PROJECT_PATH_KEY%self.spider_name_map)

    def rm(self):
        pass
