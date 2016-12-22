#coding=utf8
# 中间件经理

class ManagerMiddleware(object):

    @staticmethod
    def process(request):
        """
        通过一系列的中间件
        :param request: 请求实例
        :return:响应实例或者请求实例（抓取失败）
        """
        pass # 返回请求或者响应
