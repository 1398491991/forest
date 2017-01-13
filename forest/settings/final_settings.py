#coding=utf-8
"""不可以改变的配置文件"""

spider_start_urls_keys='forest:spider:%s:init_urls' # set list

spider_settings_keys='forest:spider:%s:settings' # map

spider_name_keys='forest:spider:names' # set

spider_status_keys='forest:spider:%s:status' # 爬虫状态  off on

spider_off_collect_request_status_keys='forest:spider:%s:collect_request_status'  # 1 ,0  # 关闭爬虫后时候同步请求

spider_off_collect_request_keys='forest:spider:%s:collect_request'  # 同步请求的 list

spider_project_path_keys='forest:spider:%s:project_path' # 需要爬虫名称 set

default_spider_settings_path='forest.settings.default_spider_settings'

default_scheduler_settings_path='forest.settings.default_scheduler_settings'

