#coding=utf-8


class Dict(dict):
    """python 基础对象的改写加强"""
    def __getattr__(self, item):
        return self[item]
