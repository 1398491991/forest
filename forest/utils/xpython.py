#coding=utf-8

from forest.decorator.misc import xdict_get


class Dict(dict):
    """python 基础对象 字典 的改写加强 强类型"""
    # def __getattr__(self, key):
    #     print key
    #     return self[key]
