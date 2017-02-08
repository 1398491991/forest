"""
Link extractor based on lxml.html
"""
import six
from six.moves.urllib.parse import urlparse, urljoin

import lxml.etree as etree

from forest.link import Link
from forest.utils.misc import arg_to_iter, rel_has_nofollow
from forest.utils.python import unique as unique_list, to_native_str
from forest.utils.response import get_base_url


# from lxml/src/lxml/html/__init__.py
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"

_collect_string_content = etree.XPath("string()")


def _nons(tag):
    if isinstance(tag, six.string_types):
        if tag[0] == '{' and tag[1:len(XHTML_NAMESPACE)+1] == XHTML_NAMESPACE:
            return tag.split('}')[-1]
    return tag

"""
scrapy.linkextractors

This package contains a collection of Link Extractors.

For more info see docs/topics/link-extractors.rst
"""
import re

from six.moves.urllib.parse import urlparse
from parsel.csstranslator import HTMLTranslator
from w3lib.url import canonicalize_url

from forest.utils.misc import arg_to_iter
from forest.utils.url import (
    url_is_from_any_domain, url_has_any_extension,
)


# common file extensions that are not followed if they occur in links
IGNORED_EXTENSIONS = [
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a',

    # office suites
    'xls', 'xlsx', 'ppt', 'pptx', 'pps', 'doc', 'docx', 'odt', 'ods', 'odg',
    'odp',

    # other
    'css', 'pdf', 'exe', 'bin', 'rss', 'zip', 'rar',
]


_re_type = type(re.compile("", 0))
_matches = lambda url, regexs: any((r.search(url) for r in regexs))
_is_valid_url = lambda url: url.split('://', 1)[0] in {'http', 'https', 'file'}


class FilteringLinkExtractor(object):

    _csstranslator = HTMLTranslator()

    def __init__(self, link_extractor, allow, deny, allow_domains, deny_domains,
                 restrict_xpaths, canonicalize, deny_extensions, restrict_css):

        self.link_extractor = link_extractor

        self.allow_res = [x if isinstance(x, _re_type) else re.compile(x)
                          for x in arg_to_iter(allow)]
        self.deny_res = [x if isinstance(x, _re_type) else re.compile(x)
                         for x in arg_to_iter(deny)]

        self.allow_domains = set(arg_to_iter(allow_domains))
        self.deny_domains = set(arg_to_iter(deny_domains))

        self.restrict_xpaths = tuple(arg_to_iter(restrict_xpaths))
        self.restrict_xpaths += tuple(map(self._csstranslator.css_to_xpath,
                                          arg_to_iter(restrict_css)))

        self.canonicalize = canonicalize
        if deny_extensions is None:
            deny_extensions = IGNORED_EXTENSIONS
        self.deny_extensions = {'.' + e for e in arg_to_iter(deny_extensions)}

    def _link_allowed(self, link):
        if not _is_valid_url(link.url):
            return False
        if self.allow_res and not _matches(link.url, self.allow_res):
            return False
        if self.deny_res and _matches(link.url, self.deny_res):
            return False
        parsed_url = urlparse(link.url)
        if self.allow_domains and not url_is_from_any_domain(parsed_url, self.allow_domains):
            return False
        if self.deny_domains and url_is_from_any_domain(parsed_url, self.deny_domains):
            return False
        if self.deny_extensions and url_has_any_extension(parsed_url, self.deny_extensions):
            return False
        return True

    def matches(self, url):

        if self.allow_domains and not url_is_from_any_domain(url, self.allow_domains):
            return False
        if self.deny_domains and url_is_from_any_domain(url, self.deny_domains):
            return False

        allowed = [regex.search(url) for regex in self.allow_res] if self.allow_res else [True]
        denied = [regex.search(url) for regex in self.deny_res] if self.deny_res else []
        return any(allowed) and not any(denied)

    def _process_links(self, links):
        links = [x for x in links if self._link_allowed(x)]
        if self.canonicalize:
            for link in links:
                link.url = canonicalize_url(urlparse(link.url))
        links = self.link_extractor._process_links(links)
        return links

    def _extract_links(self, *args, **kwargs):
        return self.link_extractor._extract_links(*args, **kwargs)


# Top-level imports


class LxmlParserLinkExtractor(object):
    def __init__(self, tag="a", attr="href", process=None, unique=False):
        self.scan_tag = tag if callable(tag) else lambda t: t == tag
        self.scan_attr = attr if callable(attr) else lambda a: a == attr
        self.process_attr = process if callable(process) else lambda v: v
        self.unique = unique

    def _iter_links(self, document):
        for el in document.iter(etree.Element):
            if not self.scan_tag(_nons(el.tag)):
                continue
            attribs = el.attrib
            for attrib in attribs:
                if not self.scan_attr(attrib):
                    continue
                yield (el, attrib, attribs[attrib])

    def _extract_links(self, selector, response_url, response_encoding, base_url):
        links = []
        # hacky way to get the underlying lxml parsed document
        for el, attr, attr_val in self._iter_links(selector.root):
            # pseudo lxml.html.HtmlElement.make_links_absolute(base_url)
            try:
                attr_val = urljoin(base_url, attr_val)
            except ValueError:
                continue # skipping bogus links
            else:
                url = self.process_attr(attr_val)
                if url is None:
                    continue
            url = to_native_str(url, encoding=response_encoding)
            # to fix relative links after process_value
            url = urljoin(response_url, url)
            link = Link(url, _collect_string_content(el) or u'',
                        nofollow=rel_has_nofollow(el.get('rel')))
            links.append(link)
        return self._deduplicate_if_needed(links)

    def extract_links(self, response):
        base_url = get_base_url(response)
        return self._extract_links(response.selector, response.url, response.encoding, base_url)

    def _process_links(self, links):
        """ Normalize and filter extracted links

        The subclass should override it if neccessary
        """
        return self._deduplicate_if_needed(links)

    def _deduplicate_if_needed(self, links):
        if self.unique:
            return unique_list(links, key=lambda link: link.url)
        return links


class LxmlLinkExtractor(FilteringLinkExtractor): # top import

    def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),
                 tags=('a', 'area'), attrs=('href',), canonicalize=True,
                 unique=True, process_value=None, deny_extensions=None, restrict_css=()):
        tags, attrs = set(arg_to_iter(tags)), set(arg_to_iter(attrs))
        tag_func = lambda x: x in tags
        attr_func = lambda x: x in attrs
        lx = LxmlParserLinkExtractor(tag=tag_func, attr=attr_func,
            unique=unique, process=process_value)

        super(LxmlLinkExtractor, self).__init__(lx, allow=allow, deny=deny,
            allow_domains=allow_domains, deny_domains=deny_domains,
            restrict_xpaths=restrict_xpaths, restrict_css=restrict_css,
            canonicalize=canonicalize, deny_extensions=deny_extensions)

    def extract_links(self, response):
        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [subdoc
                    for x in self.restrict_xpaths
                    for subdoc in response.xpath(x)]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        return unique_list(all_links)
