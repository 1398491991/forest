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