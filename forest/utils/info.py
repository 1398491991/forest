# coding=utf-8
from forest.settings.final_settings import *
from forest.db.rd import rd_conn
from forest.utils.misc import pickle_loads,pickle_dumps

class SpiderInfo(object):
    """输入爬虫名名称 获取或者设置相应的状态信息"""
    def __init__(self,spider_name):
        self.spider_name=spider_name

    def get_spider_status(self):
        """返回布尔值 不存在视为关闭"""
        if rd_conn.get(spider_status_keys%self.spider_name)=='on':
            return True
        return False

    @staticmethod
    def get_all_spider_name():
        """返回所有爬虫名称的集合 set """
        return rd_conn.smembers(spider_name_keys)

    def get_spider_project_path(self):
        """返回爬虫所有的项目路径"""
        return SpiderInfo.get_spider_project_path(self.spider_name)

    @staticmethod
    def get_spider_project_path(spider_name):
        """返回爬虫所有的项目路径 静态方法"""
        return rd_conn.smembers(spider_project_path_keys%spider_name)


    def get_spider_start_urls(self,clear=False):
        """返回爬虫开始Url的集合或者list 是否清除"""
        key=spider_start_urls_keys%self.spider_name
        t=rd_conn.type(key)
        if t=='set':
            res = rd_conn.smembers(key)
        else:
            res= rd_conn.lrange(key,0,-1)
        if clear:
            rd_conn.delete(key)
        return res

    def get_spider_download_timeout(self):
        """获取下载超时参数"""
        timeout=rd_conn.get(spider_download_timeout_keys%self.spider_name)
        if timeout is None:
            return 180 # 默认 180s

        return float(timeout)

    def get_spider_unique_user_agent(self):
        """获取爬虫独有的请求user_agent"""
        user_agent=rd_conn.get(spider_unique_user_agent_keys%self.spider_name)
        if not user_agent:
            return '' # 暂时返回空字符串
        return user_agent

    def get_unique_spider_header(self):
        # hash table
        header=rd_conn.hgetall(spider_unique_header_keys%self.spider_name)
        if not header:
            return {} #暂时的
        return header

    # def get_unique_spider_header

    def get_spider_collect_status(self):
        """关闭爬虫 是否收集正在处理的请求 下次继续"""
        if rd_conn.get(spider_off_collect_request_status_keys%self.spider_name)=='on':
            return True
        return False

    def get_spider_collect_request(self,pickle=False,clear=True):
        """返回某个爬虫收集的请求列表 序列化的 str"""
        # clear 是否清除
        def _lambda(request):
            return request

        pf=pickle_loads if pickle else _lambda
        key = spider_off_collect_request_keys % self.spider_name
        res= rd_conn.lrange(key,0,-1)
        if clear:
            rd_conn.delete(key)
        return map(pf,res)



    def get_spider_url_depth(self):
        """获取spider 的url深度 0 表示不限制"""
        depth=rd_conn.get(spider_url_depth_keys%self.spider_name)
        if not depth:
            return 0
        return int(depth)

    def get_spider_request_max_retry_count(self):
        """获取爬虫请求的最大重试次数"""
        c=rd_conn.get(spider_request_max_retry_count_keys%self.spider_name)
        if not c:
            return 3
        return int(c)


    def get_spider_redirect_status(self):
        """获取爬虫是否允许重定向"""
        c=rd_conn.get(spider_redirect_status_keys%self.spider_name)
        if c=='on':
            return True
        return False

    def get_spider_cookies(self,pickle=False):
        """获取爬虫的cookies 序列化后的 或者帮你序列化"""
        cookies=rd_conn.get(spider_cookies_keys%self.spider_name)
        if not cookies:
            cookies= '(dp0\n.'  # dict()
        return pickle_loads(cookies) if pickle else cookies

    def get_spider_url_max_length(self):
        """获取爬虫最大的Url长度  0 表示 无限制"""
        l=rd_conn.get(spider_url_max_length_keys%self.spider_name)
        if not l:
            return 0
        return int(l)

    def get_spider_url_min_length(self):
        """获取爬虫最大的Url长度  0 表示 无限制"""
        l=rd_conn.get(spider_url_min_length_keys%self.spider_name)
        if not l:
            return 0
        return int(l)

    def get_spider_bad_urls(self,clear=False):
        """死链接 会排出在外 当过多时候 不建议这全部返回 是否清除"""
        key=spider_bad_urls_keys%self.spider_name
        res=rd_conn.smembers(key)
        if clear:
            rd_conn.delete(key)
        return res

    # 以下是设置爬虫的信息^^^^^^^^^^^^^^^^^^^^^^^^^

    def set_spider_status(self,status):
        """设置爬虫的信息"""
        assert status in ['on','off']
        return rd_conn.set(spider_status_keys%self.spider_name,status)

    @staticmethod
    def set_spider_project_path(spider_name,path):
        """设置爬虫项目路径 静态方法"""
        assert isinstance(path,basestring)
        return rd_conn.sadd(spider_project_path_keys%spider_name,path)


    @staticmethod
    def set_spider_start_urls(spider_name,urls,allow_same=True,clear=False):
        """设置urls 根据spider_name  clear是否清除以前的"""
        key=spider_start_urls_keys%spider_name
        if clear:
            rd_conn.delete(key)
        f=rd_conn.rpush if allow_same else rd_conn.sadd

        return f(key,*urls)

    def set_spider_download_timeout(self,timeout):
        """设置下载超时参数"""
        assert isinstance(timeout,(int,float))
        return rd_conn.set(spider_download_timeout_keys%self.spider_name,timeout)

    def set_spider_unique_user_agent(self,user_agent):
        """设置爬虫独有的请求user_agent str"""
        # assert isinstance(user_agent,basestring)
        return rd_conn.set(spider_unique_user_agent_keys%self.spider_name,user_agent)

    def set_unique_spider_header(self,header):
        # hash table
        assert isinstance(header,dict)
        return rd_conn.hmset(spider_unique_header_keys%self.spider_name,header)


    def set_spider_collect_status(self,collect_status):
        """关闭爬虫 是否收集正在处理的请求 下次继续"""
        assert collect_status in ['on','off']
        return rd_conn.get(spider_off_collect_request_status_keys%self.spider_name,collect_status)

    def set_spider_collect_request(self,request,pickle=False,clear=False):
        """返回某个爬虫收集的请求列表 序列化的 str"""
        # clear 是否清除
        key = spider_off_collect_request_keys % self.spider_name
        if clear:
            rd_conn.delete(key)
        rd_conn.rpush(key,pickle_dumps(request) if pickle else request)

    def set_spider_url_depth(self,depth):
        """获取spider 的url深度 0 表示不限制"""
        assert isinstance(depth,int)
        return rd_conn.set(spider_url_depth_keys%self.spider_name,depth)


    def set_spider_request_max_retry_count(self,c):
        """获取爬虫请求的最大重试次数"""
        assert isinstance(c,int)
        return rd_conn.set(spider_request_max_retry_count_keys%self.spider_name,c)



    def set_spider_redirect_status(self,redirect_status):
        """获取爬虫是否允许重定向"""
        assert redirect_status in ['on', 'off']
        return rd_conn.get(spider_redirect_status_keys%self.spider_name,redirect_status)


    def set_spider_cookies(self,cookies,pickle=False):
        """设置爬虫的cookies 序列化后的 或者自动帮你序列化"""
        # assert isinstance(cookies,(basestring,dict))
        return rd_conn.set(spider_cookies_keys%self.spider_name,
                           pickle_dumps(cookies) if pickle else cookies)


    def set_spider_url_max_length(self,l):
        """获取爬虫最大的Url长度  0 表示 无限制"""
        assert isinstance(l,int)
        return rd_conn.set(spider_url_max_length_keys%self.spider_name,l)


    def set_spider_url_min_length(self,l):
        """获取爬虫最大的Url长度  0 表示 无限制"""
        assert isinstance(l,int)
        return rd_conn.set(spider_url_min_length_keys%self.spider_name,l)


    def set_spider_bad_urls(self,url,clear=False):
        """设置一个爬虫的死链接"""
        assert isinstance(url,(basestring,list,tuple))
        key = spider_bad_urls_keys%self.spider_name
        if clear:
            rd_conn.delete(key)
        if isinstance(url,basestring):
            url=[url]
        return rd_conn.sadd(key,*url)


