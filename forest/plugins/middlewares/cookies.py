#coding=utf-8

from forest.services.info import getSpiderInfo
from forest.utils.serializable import load_pickle


class CookiesMiddleware(object):
    """设置 请求的 cookies """


    def get_spider_request_cookies(self,spider_name):
        return getSpiderInfo.get_spider_request_cookies(spider_name)

    def get_spider_request_cookies_status(self,spider_name):
        return getSpiderInfo.get_spider_request_cookies_status(spider_name)

    def process_request(self,request):
        # cookies
        if not self.get_spider_request_cookies_status(request.from_spider): #静止cookies
            request.cookies=None
            return request

        if not request.cookies:
            cookies=self.get_spider_request_cookies(request.from_spider)
            if cookies:
                try:
                    cookies=load_pickle(cookies)
                except:
                    cookies={'Cookies':cookies}

                request.cookies=cookies

        return request
