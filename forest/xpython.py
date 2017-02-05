#coding=utf-8

class Dict(dict):
    def __getattr__(self, item):
        # self.1
        """有风险的针对数字 为 key"""
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        return self.__setitem__(key,value)