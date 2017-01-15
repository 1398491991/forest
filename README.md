#基于celery&redis的爬虫框架
"""
name set (str)
project set (str)
status str(on,off) (str)
start_urls list or set (str)
timeout map (int)
user_agent set (str)
header set (dict) pickle
proxy set (dict) pickle
cache list (request) pickle
去重 set (str)
深度 map (int)
retry_count map (int)
重定向 map (bool,int)
cookies map (dict) pickle
url_max_length map (int)
url_min_length map (int)
bad_urls set (str)
"""