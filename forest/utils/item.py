#coding=utf-8
from xpython import Dict

class ItemBase(Dict):
    """定义一个 保存 item 的字段 继承 Dict 暂时的"""
    pass


class ItemSave(object):
    def __init__(self,item):
        self.item=item

    def save(self):
        pass