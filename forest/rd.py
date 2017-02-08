#coding=utf-8
from redis import Redis
from redis import ConnectionError
from utils.parse_config import parseConfig
import os,sys
sys.path.append(os.path.dirname(parseConfig.config_path))

import forest_config
REDIS_CONFIG=forest_config.REDIS_CONFIG

def get_rd_conn():
    r= Redis(**REDIS_CONFIG)
    if not r.ping():
        raise ConnectionError,'redis conn failure'

    return r

rd_conn=get_rd_conn()