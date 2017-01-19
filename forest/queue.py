#coding=utf8
"""队列"""

class Base(object):
    """Per-spider queue/stack base class"""

    def __init__(self, server):
        """Initialize per-spider redis queue.

        Parameters:
            server -- redis connection
            spider -- spider instance
            key -- key for this queue (e.g. "%(spider)s:queue")

        """
        self.server = server

    def __len__(self,key):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, key ,obj):
        """Push a obj"""
        raise NotImplementedError

    def pop(self, key ,timeout=0):
        """Pop a obj"""
        raise NotImplementedError



class Queue(Base):
    """Per-spider FIFO queue"""

    def __len__(self,key):
        """Return the length of the queue"""
        return self.server.llen(key)

    def push(self, key,obj):
        """Push a obj"""
        return self.server.lpush(key, obj)

    def pop(self, key,timeout=0):
        """Pop a obj"""
        if timeout > 0:
            data = self.server.brpop(key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(key)
        return data


class PriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""

    def __len__(self,key):
        """Return the length of the queue"""
        return self.server.zcard(key)

    def push(self, key ,obj,**kwargs):
        """Push a obj"""
        priority=kwargs.pop('priority',0)
        return self.server.execute_command('ZADD', key, priority, obj)

    def pop(self, key,timeout=0):
        """
        Pop a obj
        timeout not support in this queue class
        """
        # use atomic range/remove using multi/exec
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(key, 0, 0).zremrangebyrank(key, 0, 0)
        results, count = pipe.execute()
        return results[0] if results else None


class StackQueue(Base):
    """Per-spider stack"""

    def __len__(self,key):
        """Return the length of the stack"""
        return self.server.llen(key)

    def push(self,key, obj):
        """Push a obj"""
        return self.server.lpush(key, obj)

    def pop(self,key, timeout=0):
        """Pop a obj"""
        if timeout > 0:
            data = self.server.blpop(key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(key)

        return data