#coding=utf-8
from forest.spider.plain import PlainSpider
from forest.http.response import Response
from forest.http.request import Request
from forest.async import async
import copy
import six

def identity(x):
    return x


class Rule(object):

    def __init__(self, link_extractor, callback=None, follow=None, process_links=None, process_request=identity):
        self.link_extractor = link_extractor
        self.callback = callback or 'parse'
        self.process_links = process_links# or 'process_links'
        self.process_request = process_request# or 'process_links'
        if follow is None:
            self.follow = False if callback else True
        else:
            self.follow = follow


class RulesSpider(PlainSpider):

    rules = []


    @async
    def parse(self, response):
        print response
        seen = set()
        res_request=set()

        for n, rule in enumerate(self.rules):
            print rule.link_extractor.extract_links(response)
            # links = [lnk for lnk in rule.link_extractor.extract_links(response)
            #          if lnk not in seen]
            # if links and rule.process_links:
            #     links = getattr(self,rule.process_links)(links)
            # for link in links:
            #     seen.add(link)
            #     r = Request(url=link.url, callback=rule.callback)
            #     res_request.add(r)

        return res_request


    def parse_start_url(self, response):
        return []

    def process_results(self, response, results):
        return results

    def _requests_to_follow(self, response):
        if not isinstance(response, Response):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = getattr(self,rule.process_links)(links)
            for link in links:
                seen.add(link)
                r = Request(url=link.url, callback=self._response_downloaded)
                r.meta.update(rule=n, link_text=link.text)
                yield rule.process_request(r)

    def _response_downloaded(self, response):
        rule = self.rules[response.meta['rule']]
        return self._parse_response(response, rule.callback, rule.cb_kwargs, rule.follow)

    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item

        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                yield request_or_item


    def __repr__(self):
        return '<RulesSpider [%s]>' % (self.name)