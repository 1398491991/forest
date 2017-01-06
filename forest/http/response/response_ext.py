#coding=utf-8
"""
将requests 的返回响应 进行包装  扩展功能
"""

class ResponseExt(object):
    def __init__(self,response):
        self.response=response
