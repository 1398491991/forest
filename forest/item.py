#coding=utf-8
from utils.serializable import dump_json
from forest.xpython import Dict

class Item(Dict):


    def to_json(self):
        return dump_json(self)

    def to_dict(self):
        return self

# if __name__ == '__main__':
#     I=Item({'1':2})
#     I.abc=1
#     print I.to_dict()
#     print I.to_json()