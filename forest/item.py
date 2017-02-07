#coding=utf-8

from utils.serializable import dump_json

class Item(dict):
    def __getattr__(self, item):
        # self.1
        """有风险的针对数字 为 key"""
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        return self.__setitem__(key,value)


    def to_json(self):
        return dump_json(self)


    def to_dict(self):
        return self



# if __name__ == '__main__':
#     I=Item(**{'1':2})
#     I.abc=1
#     print I.to_dict()
#     print I.to_json()