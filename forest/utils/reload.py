# coding=utf-8
"""基于 redis"""
from spider import get_spider_project_path

class ReLoad(object):
    """根据爬虫名来重新导入环境，从而免去重启调度器的问题"""
    def __init__(self,name):
        self.name=name

    def reload(self):
        # run
        return self.traversal_and_reload()


    def traversal_and_reload(self):
        """遍历该包（模块）并且reload"""
        p=__import__(get_spider_project_path(self.name))
        d=p.__dict__
        # assert isinstance(d,dict)
        for k,v in d.items():
            # assert isinstance(v,str)
            if v.startswith('<module'):
                try:
                    reload(getattr(p,k))
                except (AttributeError,ImportError):
                    pass

import threading
import time
from spider import get_all_reload_spider_name

class ReLoadThread(threading.Thread):
    """监控 reload 的线程"""
    def run(self):
        ss=get_all_reload_spider_name()
        for s in ss:
            ReLoad(s).reload()
        time.sleep(3) # todo 暂时的 3s 刷新一次




