#coding=utf-8


import posixpath
from six.moves.urllib.parse import (ParseResult, urldefrag, urlparse)
from scrapy.utils.python import to_unicode


def url_is_from_any_domain(url, domains):
    """Return True if the url belongs to any of the given domains"""
    host = parse_url(url).netloc.lower()
    if not host:
        return False
    domains = [d.lower() for d in domains]
    return any((host == d) or (host.endswith('.%s' % d)) for d in domains)

def parse_url(url, encoding=None):
    """Return urlparsed url from the given argument (which could be an already
    parsed url)
    """
    if isinstance(url, ParseResult):
        return url
    return urlparse(to_unicode(url, encoding))

def url_has_any_extension(url, extensions):
    return posixpath.splitext(parse_url(url).path)[1].lower() in extensions