#coding=utf-8

from forest.decorator.misc import error_val


class Dict(dict):
    """python 基础对象 字典 的改写加强 强类型"""
    # def __getattr__(self, key):
    #     print key
    #     return self[key]


    @error_val(0)
    def getint(self,key):
        pass

    @error_val(0.0)
    def getfloat(self,key):
        pass


    @error_val('')
    def getstr(self,key):
        pass

    @error_val(dict())
    def getdict(self,key):
        pass

    @error_val([])
    def getlist(self,key):
        pass


    @error_val(set())
    def getset(self,key):
        pass

    @error_val(tuple())
    def gettuple(self,key):
        pass




if __name__ == '__main__':
    d=Dict({'a':1,'b':2,'c':{1:2}})
    print d.gettuple('a',ignore_exist=False)