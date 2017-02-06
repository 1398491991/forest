#coding=utf-8

REDIS_CONFIG={'host':'10.0.0.12'}

DEFAULT_SSH_LOG_CONFIG={'filename':'ssh.log','level':'DEBUG'}

SLAVE_NAMES_KEY='forest:slave_names' # set

APPOINT_QUEUE_REQUEST_KEY='forest:appoint_queue:%(hostname)s:request'
PUBLIC_PRIORITY_QUEUE_REQUEST_KEY='forest:public_priority_queue:request'
PUBLIC_QUEUE_REQUEST_KEY='forest:public_queue:request'

SPIDER_INSTANCE_KEY='forest:spider_instance:%(spider_name)s'
SPIDER_NAME_KEY='forest:spider_name' # set
SPIDER_PROJECT_PATH_KEY='forest:%(spider_name)s:spider_project_path' # set
SPIDER_URL_MAX_LENGTH_KEY='forest:%(spider_name)s:url_max_length' # map
SPIDER_URL_MIN_LENGTH_KEY='forest:%(spider_name)s:url_min_length' # map
SPIDER_RETRY_COUNT_KEY='forest:%(spider_name)s:retry_count' # map
SPIDER_REQUEST_TIMEOUT_KEY='forest:%(spider_name)s:timeout' # map
SPIDER_REQUEST_HEADERS_KEY='forest:%(spider_name)s:request_headers' # HSET
SPIDER_REQUEST_USER_AGENT_KEY='forest:%(spider_name)s:user_agent' # set

DEFAULT_SPIDER_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DEFAULT_SPIDER_REQUEST_TIMEOUT=180
DEFAULT_SPIDER_REQUEST_USER_AGENT='forest'
DEFAULT_SPIDER_URL_MAX_LENGTH=0 # 0 表示没有限制
DEFAULT_SPIDER_URL_MIN_LENGTH=0 # 0 表示没有限制
DEFAULT_SPIDER_RETRY_COUNT=3

DEFAULT_TASK_NULL_ACTION_SLEEP_TIME=5
TASK_NULL_ACTION_SLEEP_TIME_KEY='forest:task_null_action_sleep_time' # map

APPOINT_QUEUE_ITEM_KEY='forest:appoint_queue:%(hostname)s:item'
PUBLIC_PRIORITY_QUEUE_ITEM_KEY='forest:public_priority_queue:%(hostname)s:item'
PUBLIC_QUEUE_ITEM_KEY='forest:public_queue:%(hostname)s:item'


PARALLEL_PRODUCER_REQUEST_COUNT_KEY='forest:%(hostname)s:PARALLEL_PRODUCER_REQUEST_COUNT_KEY'
PARALLEL_PRODUCER_ITEM_COUNT_KEY='forest:%(hostname)s:PARALLEL_PRODUCER_ITEM_COUNT_KEY'

DEFAULT_PARALLEL_PRODUCER_REQUEST_COUNT=5
DEFAULT_PARALLEL_PRODUCER_ITEM_COUNT=5

PARALLEL_JOB_ITEM_COUNT_KEY='forest:%(hostname)s:PARALLEL_JOB_ITEM_COUNT'
PARALLEL_JOB_REQUEST_COUNT_KEY='forest:%(hostname)s:PARALLEL_JOB_REQUEST_COUNT'


DEFAULT_PARALLEL_JOB_REQUEST_COUNT=1
DEFAULT_PARALLEL_JOB_ITEM_COUNT=1



JOB_REQUEST_PID_KEY='forest:%(hostname)s:request_pids'
JOB_ITEM_PID_KEY='forest:%(hostname)s:item_pids'

from forest.utils.misc import get_host_name
LOCAL_HOST_NAME=get_host_name()