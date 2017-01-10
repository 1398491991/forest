# coding=utf-8

class CallbackTypeException(Exception):
    """返回的Http类型错误"""
    pass

class ProjectPathNotExistsException(Exception):
    """项目路径不存在错误"""
    def __repr__(self):
        return '<%s>'%self.args

    __str__=__repr__

class RegisterSpiderException(Exception):
    """注册爬虫错误"""
    def __repr__(self):
        return '<%s>'%self.args

    __str__=__repr__


class AsyncResultNotIterException(Exception):
    """针对返回的异步过程 必须是可迭代的 列表等等"""
    def __repr__(self):
        return '<%s>'%self.args

    __str__=__repr__


class DiscardException(Exception):
    """抛弃  中间件处理"""
    def __init__(self,obj=None,reason=None):
        self.obj=obj
        self.reason=reason


    def __repr__(self):
        return '<%s:%s>'%(self.obj,self.reason)

    __str__=__repr__