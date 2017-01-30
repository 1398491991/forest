#coding=utf-8

REDIS_CONFIG={}

SSH_LOG_CONFIG={'filename':'ssh.log','level':'DEBUG'}


APPOINT_QUEUE_REQUEST_KEY='forest:appoint_queue:%(hostname)s:request'
PUBLIC_PRIORITY_QUEUE_REQUEST_KEY='forest:public_priority_queue:%(hostname)s:request'
PUBLIC_QUEUE_REQUEST_KEY='forest:public_queue:%(hostname)s:request'

SPIDER_INSTANCE_KEY='forest:spider_instance:%(spider_name)'

APPOINT_QUEUE_ITEM_KEY='forest:appoint_queue:%(hostname)s:item'
PUBLIC_PRIORITY_QUEUE_ITEM_KEY='forest:public_priority_queue:%(hostname)s:item'
PUBLIC_QUEUE_ITEM_KEY='forest:public_queue:%(hostname)s:item'


MAX_PROCESS_REQUEST_COUNT_KEY='forest:%(hostname)s:max_process_request_count'
DEFAULT_MAX_PROCESS_REQUEST_COUNT=10

MAX_PROCESS_ITEM_COUNT_KEY='forest:%(hostname)s:max_process_item_count'
DEFAULT_MAX_PROCESS_ITEM_COUNT=10

MAX_PROCESS_COUNT_KEY='forest:%(hostname)s:max_process_count'
DEFAULT_MAX_PROCESS_COUNT=3

JOB_REQUEST_PID_KEY='forest:%(hostname)s:request_pids'
JOB_ITEM_PID_KEY='forest:%(hostname)s:item_pids'