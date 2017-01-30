#coding=utf-8
from utils.serializable import dump_json

class SimpleItem(dict):

    def __getattr__(self, item):
        # self.1
        """有风险的针对数字 为 key"""
        return self.__getitem__(item)

    def to_json(self):
        return dump_json(self)

    def to_dict(self):
        return self

Item=SimpleItem

# if __name__ == '__main__':
#     I=Item({'1':2})
#     print I.to_dict()
#     print I.to_json()