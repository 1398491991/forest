#coding=utf-8
import sys
from celery import Celery


class MyCelery(Celery):
    # pass
    def task(self,*args, **opts):
        self.update_sys_path()
        return super(MyCelery,self).task(*args,**opts)

    def update_sys_path(self):
        if 'f:/forest/example/' not in sys.path:
            print '\n*****************************\n'
            sys.path.append('f:/forest/example/')