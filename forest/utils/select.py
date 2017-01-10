#coding=utf-8
"""
将requests 的返回响应 进行包装  扩展功能
"""

from parsel import Selector as _ParselSelector,SelectorList as _ParselSelectorList

class SelectorList(_ParselSelectorList):

    def extract_last(self, default=None):
        """
        Return the result of ``.extract()`` for the first element in this list.
        If the list is empty, return the default value.
        """
        for x in self[-1::-1]:
            return x.extract()
        else:
            return default

class Selector(_ParselSelector):
    """待实现"""
    selectorlist_cls = SelectorList



