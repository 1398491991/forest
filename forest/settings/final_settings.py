#coding=utf-8
"""不可以改变的配置文件"""

spider_start_urls_keys='forest:spider:%s:start_urls' # set list

spider_download_timeout_keys='forest:spider:%s:download_timeout' #map int

spider_unique_user_agent_keys='forest:spider:%s:user_agent' #map str

spider_unique_header_keys='forest:spider:%s:header' # hash table str

spider_url_depth_keys='forest:spider:%s:url_depth' # map int

spider_request_max_retry_count_keys='forest:spider:%s:request_max_retry_count' # map int

spider_redirect_status_keys='forest:spider:%s:redirect_status' # map str

spider_cookies_keys='forest:spider:%s:cookies' # map str

spider_url_max_length_keys='forest:spider:%s:url_max_length' # map int

spider_url_min_length_keys='forest:spider:%s:url_min_length' # map int

spider_bad_urls_keys='forest:spider:%s:bad_urls' # set str

spider_user_agent_keys='forest:spider:user_agent' #set str

spider_settings_keys='forest:spider:%s:settings' # map

spider_name_keys='forest:spider:names' # set

spider_status_keys='forest:spider:%s:status' # 爬虫状态  off on

spider_off_collect_request_status_keys='forest:spider:%s:collect_request_status'  # 1 ,0  # 关闭爬虫后时候同步请求

spider_off_collect_request_keys='forest:spider:%s:collect_request'  # 同步请求的 list

spider_project_path_keys='forest:spider:%s:project_path' # 需要爬虫名称 set

default_spider_settings_path='forest.settings.default_spider_settings'

default_scheduler_settings_path='forest.settings.default_scheduler_settings'

