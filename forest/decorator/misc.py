#coding=utf-8
from functools import wraps

def error_val(default_val,ignore_exist=False):
    #  针对 xpython Dict
    #　键值或者类型错误返回的值
    def wrapper(fun):

        @wraps(fun)
        def _wrapper(self,key):
            try:
                result=self[key]
            except KeyError:
                return default_val
            else:
                if type(default_val)!=type(result):
                    if ignore_exist:
                        return default_val
                    else:
                        raise ValueError(u'键值存在，获取类型错误 %s'%type(result))
                return result
        return _wrapper
    return wrapper


import sys

def update_sys_path(func):
    """添加搜素路径遍历 针对 task"""
    print func.__name__,func
    print '@@@@@@@@@@@@@@@@@@@'
    @wraps(func)
    def wrapper(*args,**kwargs):
        print '###################'
        if 'f:/forest/example/' not in sys.path:
            print '\n*****************************\n'
            sys.path.append('f:/forest/example/')
        return func(*args,**kwargs)
    return wrapper