#coding=utf-8

REDIS_CONFIG={}

SSH_LOG_CONFIG={'filename':'ssh.log','level':'DEBUG'}


APPOINT_QUEUE_REQUEST_KEY='forest:appoint_queue:%(hostname)s:request'
PUBLIC_PRIORITY_QUEUE_REQUEST_KEY='forest:public_priority_queue:request'
PUBLIC_QUEUE_REQUEST_KEY='forest:public_queue:request'

SPIDER_INSTANCE_KEY='forest:spider_instance:%(spider_name)s'

APPOINT_QUEUE_ITEM_KEY='forest:appoint_queue:%(hostname)s:item'
PUBLIC_PRIORITY_QUEUE_ITEM_KEY='forest:public_priority_queue:%(hostname)s:item'
PUBLIC_QUEUE_ITEM_KEY='forest:public_queue:%(hostname)s:item'


PARALLEL_PRODUCER_REQUEST_SIZE_KEY='forest:%(hostname)s:PARALLEL_PRODUCER_REQUEST_SIZE_KEY'
PARALLEL_PRODUCER_ITEM_SIZE_KEY='forest:%(hostname)s:PARALLEL_PRODUCER_ITEM_SIZE_KEY'

DEFAULT_PARALLEL_PRODUCER_REQUEST_SIZE=5
DEFAULT_PARALLEL_PRODUCER_ITEM_SIZE=5

PARALLEL_JOB_ITEM_SIZE_KEY='forest:%(hostname)s:PARALLEL_JOB_ITEM_SIZE'
PARALLEL_JOB_REQUEST_SIZE_KEY='forest:%(hostname)s:PARALLEL_JOB_REQUEST_SIZE'


DEFAULT_PARALLEL_JOB_REQUEST_SIZE=1
DEFAULT_PARALLEL_JOB_ITEM_SIZE=1



JOB_REQUEST_PID_KEY='forest:%(hostname)s:request_pids'
JOB_ITEM_PID_KEY='forest:%(hostname)s:item_pids'

from forest.utils.misc import get_host_name
LOCAL_HOST_NAME=get_host_name()