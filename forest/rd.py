#coding=utf-8
from redis import Redis
import config
REDIS_CONFIG=config.REDIS_CONFIG

def get_rd_conn():
    return Redis(**REDIS_CONFIG)

rd_conn=get_rd_conn()