#coding=utf-8
from forest.db.rd import rd_conn
import os
from forest.utils.exceptions import RegisterSpiderException,ProjectPathNotExistsException


def register_spider(project_path):
    """注册爬虫"""
    if not os.path.exists(project_path):
        return ProjectPathNotExistsException # 项目路径不存在
    try:
        # 注册成功返回注册的条数
        return rd_conn.sadd('forest:spiders:project_path_register')

    except:
        return RegisterSpiderException

def eliminate_spider(project_path):
    """排除爬虫"""
    pass
