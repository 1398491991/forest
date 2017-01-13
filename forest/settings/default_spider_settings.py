#coding=utf-8
"""爬虫的默认配置文件"""

middleware={
    'forest.middleware.retry.RetryMiddleware':8,
    'forest.middleware.timeout.DownLoadTimeOutMiddleware':9,
    'forest.middleware.headers.HeadersMiddleware':10,
    'forest.middleware.useragent.UserAgentMiddleware':11,
    'forest.middleware.httpproxy.HttpProxyMiddleware':12,
    'forest.middleware.download.DownLoadMiddleware':1000, # 一定最大
}

pipeline='forest.pipeline.pipeline.Pipeline'

retry_max_count=3

request_headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

download_timeout=180

user_agent='forest'
