#coding=utf-8
from demo3 import Demo
# celery -A forest.scheduler.tasks worker --loglevel=info
# from forest.http import ResponseBase
from forest.utils.register import RegisterSpider
d=Demo.config_from_py(None)
regs=RegisterSpider(d)
regs.register()
d.start_urls_to_redis()
d.start()