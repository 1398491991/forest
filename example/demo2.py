from demo import Demo

d=Demo.config_from_py(None)
d.start()
d.run1()
#
# from scrapy import Request
# class a(object):
#     def run1(self):
#         import pickle
#         pickle.dumps(Request('http://www.baidu.com',callback=self.run2))
#
#
#     def run2(self):
#         pass
#
# a().run1()
