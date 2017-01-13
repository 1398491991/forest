#coding=utf-8
from forest.utils.spider import get_all_sys_path
from forest.utils.misc import update_sys_path
import sys

def sys_path_sync_patch(func):
    """环境变量同步补丁 主要是给序列化过程使用"""
    def wrapper(*args,**kwargs):
        s1,s2=get_all_sys_path()
        # todo 同步一下环境变量
        sys.path=update_sys_path(sys.path,s1,method='add')
        sys.path=update_sys_path(sys.path,s2,method='remove')
        return func(*args,**kwargs)
    return wrapper