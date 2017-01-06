#coding=utf-8
"""一个关系型数据库使用的简便包装"""
import MySQLdb

db_config={
    'host':'localhost',
    'user':'root',
    'passwd':'123456789',
    'db':'lshu',
    'port':3306,
    'charset':'utf8'
}
# 暂时初始化方法
ms_conn=MySQLdb.connect(**db_config)

class MsWrapper(object):
    pass