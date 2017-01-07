#coding=utf-8

from forest.decorator.misc import xdict_get


class Dict(dict):
    """python 基础对象 字典 的改写加强 强类型"""
    # def __getattr__(self, key):
    #     print key
    #     return self[key]


    @xdict_get(0)
    def getint(self,key):
        pass

    @xdict_get(0.0)
    def getfloat(self,key):
        pass


    @xdict_get('')
    def getstr(self,key):
        pass

    @xdict_get(dict())
    def getdict(self,key):
        pass

    @xdict_get([])
    def getlist(self,key):
        pass


    @xdict_get(set())
    def getset(self,key):
        pass

    @xdict_get(tuple())
    def gettuple(self,key):
        pass




if __name__ == '__main__':
    d=Dict({'a':1,'b':2,'c':{1:2}})
    print d.gettuple('a',ignore_exist=False)