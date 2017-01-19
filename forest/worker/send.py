#coding=utf-8
try:
    import gevent
    from gevent import monkey as curious_george
    from gevent.pool import Pool
except ImportError:
    raise RuntimeError('Gevent is required for grequests.')
import requests
from ..http.response import Response
from ..utils.select import Selector
# Monkey-patch.
curious_george.patch_all(thread=False, select=False)

BASE_REQUEST_PARAMS=['method','url','headers','files',
    'data','params','auth','cookies','hooks','json',]

EXTEND_REQUEST_PARAMS=['from_spider','callback','project_path','replace_optional',
                 'priority','appoint_name','meta',]



def bind(response,request):
    """绑定对象到响应"""
    select=Selector(response.text,base_url=response.url)
    return Response(response,select)



class Send(object):


    def send(self,r, pool=None, stream=False):
        """Sends the request object using the specified pool. If a pool isn't
        specified this method blocks. Pools are useful because you can specify size
        and can hence limit concurrency."""

        def send(r):

            kwargs = {k:r[k] for k in BASE_REQUEST_PARAMS}
            kwargs.update({'stream':stream})
            try:
                response = requests.request(**kwargs)
                map(lambda x:setattr(response,x,r[x]),EXTEND_REQUEST_PARAMS)
                return bind(response,r)

            except:
                return r

        if pool is not None:
            return pool.spawn(send,r)

        return gevent.spawn(send,r)


    def map(self,requests, stream=False, size=None, exception_handler=None, gtimeout=None):
        """Concurrently converts a list of Requests to Responses.

        :param requests: a collection of Request objects.
        :param stream: If True, the content will not be downloaded immediately.
        :param size: Specifies the number of requests to make at a time. If None, no throttling occurs.
        :param exception_handler: Callback function, called when exception occured. Params: Request, Exception
        :param gtimeout: Gevent joinall timeout in seconds. (Note: unrelated to requests timeout)
        """
        _requests = list(requests)
        pool = Pool(size) if size else None
        jobs = [self.send(r, pool, stream=stream) for r in _requests]
        res=gevent.joinall(jobs, timeout=gtimeout)
        return map(lambda x:x.value,res)