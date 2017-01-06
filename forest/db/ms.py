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
def get_ms_conn(db_config):
    return MySQLdb.connect(**db_config)

ms_conn=get_ms_conn(db_config)

class MsWrapper(object):
    """封装 mysql 操作"""
    def __init__(self,db_config):
        self.conn=MySQLdb.connect(**db_config)
        self.cursor = self.conn.cursor()

    def runSql(self,sql,params=None,**kwargs):
        return self.cursor.execute(sql,params,**kwargs)


    def commitSql(self):
        self.conn.commit()

    def runQuery(self,sql,params=None,**kwargs):
        self.runSql(sql,params,**kwargs)
        return self.cursor.fetchall() # 返回元组


    def runQueryDict(self,sql,params=None):
        cur=self.conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(sql,params)
        return cur.fetchall() # 返回字典


    def get_ms_new_conn(self,_db_config=None):
        return get_ms_conn(_db_config or db_config)

    def reconnect_ms(self):
        self.conn=self.get_ms_new_conn()


    def close(self):
        self.cursor.close()
        self.conn.close()


    def connClose(self):
        self.conn.close()


    def cursorClose(self):
        self.cursor.close()