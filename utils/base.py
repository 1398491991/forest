#coding=utf-8
import time
import weakref
from collections import defaultdict
NoneType = type(None)
live_refs = defaultdict(weakref.WeakKeyDictionary)


class object_ref(object):
    """Inherit from this class (instead of object) to a keep a record of live
    instances"""

    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        live_refs[cls][obj] = time.time()
        return obj