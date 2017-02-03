# coding=utf-8
"""
添加 spider 各项指标的方法集合
"""
from ..rd import rd_conn
import config
from ..utils.serializable import load_json

SPIDER_NAME_KEY=config.SPIDER_NAME_KEY
SPIDER_PROJECT_PATH_KEY=config.SPIDER_PROJECT_PATH_KEY
RETRY_COUNT=config.RETRY_COUNT
URL_MAX_LENGTH=config.URL_MAX_LENGTH
URL_MIN_LENGTH=config.URL_MIN_LENGTH
SPIDER_INSTANCE_KEY=config.SPIDER_INSTANCE_KEY


class AddSpider(object):


    def __init__(self,info,transaction=True):
        if isinstance(info,basestring):
            info=load_json(info)

        self.info=info

        self.rd_conn=rd_conn.pipeline(transaction)

    def add(self):
        pass



    def add_spider_instance(self):
        pass


    def add_spider_name(self):
        pass

    def add_spider_project_path(self):
        pass

    def add_retry_count(self):
        pass

    def add_url_max_length(self):
        pass

    def add_url_min_length(self):
        pass

    # def add_cook




class AddBase(object):

    def __init__(self,spider_name):
        assert isinstance(spider_name,basestring) and spider_name
        self.spider_name=spider_name
        self.spider_name_key=SPIDER_NAME_KEY

    @property
    def rd_conn(self):
        return rd_conn

    def add(self,pipe):
        # pipe = self.rd_conn.pipeline() # 事务处理
        raise NotImplementedError

class AddSpiderInstance(AddBase):
    def __init__(self,spider_name,spider_instance_pickle):

        super(AddSpiderInstance,self).__init__(spider_name)

        assert isinstance(spider_instance_pickle,basestring)
        self.spider_instance_pickle=spider_instance_pickle

        self.spider_instance_key=SPIDER_INSTANCE_KEY%{'spider_name':spider_name}


    def add(self,pipe):
        # pipe = self.rd_conn.pipeline()
        self.exists()
        pipe.set(self.spider_instance_key,self.spider_instance_pickle)


    def exists(self):
        if self.rd_conn.exists(self.spider_instance_key):
            raise Exception,'spider %s exist'%self.spider_name

class AddSpiderName(AddBase):

    def add(self,pipe):
        # pipe = self.rd_conn.pipeline()
        self.exists()
        pipe.sadd(self.spider_name_key,self.spider_name)

    def exists(self):
        if self.spider_name in self.rd_conn.smembers(self.spider_name_key):
            raise Exception,'spider %s exist'%self.spider_name

class AddSpiderProjectPath(AddBase):

    def __init__(self,spider_name,project_path):

        super(AddSpiderProjectPath,self).__init__(spider_name)

        if isinstance(project_path,basestring):
            project_path=[project_path]
        self.project_path=project_path
        self.spider_project_path_key=SPIDER_PROJECT_PATH_KEY%{'spider_name':spider_name}

    def add(self,pipe):
        # pipe = self.rd_conn.pipeline()
        self.exist()
        pass

    def exist(self):
        if self.rd_conn.exists(self.spider_project_path_key):
            raise Exception,'spider %s exist'%self.spider_name