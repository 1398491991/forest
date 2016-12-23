# import scrapy
# from forest.http import Request
from forest.core.scheduler.scheduler import process_request
# import pickle

class a:
    pass

class test(object):
    def run1(self,response=None):
        print response,'####################'
        process_request.delay({'url':'http://www.baidu.com','callback':'run2','self':self.__class__})

    def run2(self,response):
        print response,'@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        process_request.delay({'url':'http://www.baidu.com','callback':'run1','self':self.__class__})
