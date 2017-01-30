#coding=utf8
"""队列"""

class QueueBase(object):
    """Per-spider queue/stack base class"""

    def __init__(self, server):
        """Initialize per-spider redis queue.

        Parameters:
            server -- redis connection
            spider -- spider instance
            key -- key for this queue (e.g. "%(spider)s:queue")

        """
        self.server = server

    def pipeline(self):
        return self.server.pipeline()


    def __len__(self,key):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, key ,obj):
        """Push a obj"""
        raise NotImplementedError

    def pop(self, key ,timeout=0):
        """Pop a obj"""
        raise NotImplementedError



class PlainQueue(QueueBase):
    """简单的先进先出队列"""

    def __len__(self,key):
        """Return the length of the queue"""
        return self.server.llen(key)

    def push(self, key,obj,x=False):
        """Push a obj"""
        if x:
            # LPUSHX key value
            # 在前面加上一个值列表，仅当列表中存在
            return self.server.lpushx(key,obj) # 添加失败返回 0

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


class PriorityQueue(QueueBase):
    """一个优先级队列  根据 redis 的有序集合实现"""

    def __len__(self,key):
        """Return the length of the queue"""
        return self.server.zcard(key)

    def push(self, key ,obj,x=False,**kwargs):
        """Push a obj"""
        if x and not self.server.exists(key):
            # 键值不存在 不插入
            return 0
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


class StackQueue(QueueBase):
    """Per-spider stack"""

    def __len__(self,key):
        """Return the length of the stack"""
        return self.server.llen(key)

    def push(self,key, obj,x=False):
        """Push a obj"""
        if x:
            return self.server.lpushx(key,obj) # 失败 返回 0

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

from rd import rd_conn

stackQueue=StackQueue(rd_conn)
priorityQueue=PriorityQueue(rd_conn)
plainQueue=PlainQueue(rd_conn)