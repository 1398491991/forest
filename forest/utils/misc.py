#coding=utf-8

from importlib import import_module
import six
from forest.item import Item


_ITERABLE_SINGLE_VALUES = dict, Item, six.text_type, bytes


def rel_has_nofollow(rel):
    """Return True if link rel attribute has nofollow type"""
    return True if rel is not None and 'nofollow' in rel.split() else False

def arg_to_iter(arg):
    """Convert an argument to an iterable. The argument can be a None, single
    value, or an iterable.

    Exception: if arg is a dict, [arg] will be returned
    """
    if arg is None:
        return []
    elif not isinstance(arg, _ITERABLE_SINGLE_VALUES) and hasattr(arg, '__iter__'):
        return arg
    else:
        return [arg]

def load_object(path):
    """Load an object given its absolute object path, and return it.

    object can be a class, function, variable or an instance.
    path ie: 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'
    """

    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot+1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" % (module, name))

    return obj

import socket


def get_host_name():
    return socket.getfqdn(socket.gethostname())


def get_host_ip():
    return socket.gethostbyname(get_host_name())
