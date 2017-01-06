#coding=utf-8
from functools import wraps

def error_val(default_val):
    #  针对 xpython Dict
    #　键值或者类型错误返回的值
    def wrapper(fun):

        @wraps(fun)
        def _wrapper(self,key,ignore_exist=False):
            try:
                result=self[key]
            except KeyError:
                return default_val
            else:
                if type(default_val)!=type(result):
                    if ignore_exist:
                        return default_val
                    else:
                        raise ValueError('key exists , type error %s'%type(result))
                return result
        return _wrapper
    return wrapper


import sys
import os
def update_sys_path(rd_conn):
    """添加搜素路径遍历 针对 task"""

    def wrapper(func):
        @wraps(func)
        def _wrapper(*args,**kwargs):
            path_set=rd_conn.smembers('forest:spider:project_path')
            for path in path_set:
                if os.path.exists(path) and path not in sys.path:
                    sys.path.append(path)
            return func(*args,**kwargs)
        return _wrapper
    return wrapper