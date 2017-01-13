#coding=utf-8
from demo2 import Demo
from forest.http import ResponseBase
d=Demo.config_from_py(None)
d.start()
d.run1(ResponseBase())