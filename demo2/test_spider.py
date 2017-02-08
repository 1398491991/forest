
from forest.spider.plain import RulesSpider
from forest.async import async
from forest.http.request import Request
from forest.spider.plain import Rule
from forest.lxmlhtml import LxmlLinkExtractor


class testSpider(RulesSpider):
    name='demo2'
    rules = [Rule(link_extractor=LxmlLinkExtractor(),)]