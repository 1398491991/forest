#coding=utf-8

class Pipeline(object):
    # example
    def __init__(self,settings):
        self.settings=settings

    def process_item(self,item):
        print 'process_item #^^^^^^^^^^^^^&&&&&&&&&&&&&&&&&&&&&'

    @classmethod
    def from_settings(cls,settings):
        return cls(settings)