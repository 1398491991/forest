
from forest.spider.rule import RulesSpider
from forest.async import async
from forest.http.request import Request
from forest.spider.rule import Rule
from forest.lxmlhtml import LxmlLinkExtractor


class testSpider(RulesSpider):
    name='demo2'
    rules = [Rule(link_extractor=LxmlLinkExtractor(),)]