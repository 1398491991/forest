#coding=utf-8
import sys
import os

DEFAULT_CONFIG_PATH=os.path.dirname(os.path.abspath(__file__))
CUSTOM_CONFIG_PATH=r'C:\Users\lshu\Desktop'
sys.path.append(CUSTOM_CONFIG_PATH or DEFAULT_CONFIG_PATH)


REDIS_CONFIG={}

SSH_LOG_CONFIG={'filename':'ssh.log','level':'DEBUG'}


APPOINT_QUEUE_REQUEST_KEY='forest:appoint_queue:%(hostname)s:request'
PUBLIC_PRIORITY_QUEUE_REQUEST_KEY='forest:public_priority_queue:%(hostname)s:request'
PUBLIC_QUEUE_REQUEST_KEY='forest:public_queue:%(hostname)s:request'


APPOINT_QUEUE_ITEM_KEY='forest:appoint_queue:%(hostname)s:item'
PUBLIC_PRIORITY_QUEUE_ITEM_KEY='forest:public_priority_queue:%(hostname)s:item'
PUBLIC_QUEUE_ITEM_KEY='forest:public_queue:%(hostname)s:item'


MAX_PROCESS_REQUEST_COUNT_KEY='forest:%(hostname)s:max_process_request_count'
DEFAULT_MAX_PROCESS_REQUEST_COUNT=10

MAX_PROCESS_ITEM_COUNT_KEY='forest:%(hostname)s:max_process_item_count'
DEFAULT_MAX_PROCESS_ITEM_COUNT=10