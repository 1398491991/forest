#coding=utf-8
from ConfigParser import SafeConfigParser
import os
import sys

class CustomConfigNotExistException(Exception):
    def __init__(self,path):
        self.path=path

    def __repr__(self):
        return 'config path "%s" not exist'%self.path

    __str__=__repr__



class ParseConfig(object):

    default_config_path=r'd:\forest\forest\config.ini'
    # default_config_path='/mnt/hgfs/project/forest/forest/config.ini'

    def __init__(self):
        self.cf=SafeConfigParser()
        self.cf.read(self.default_config_path)

        self.config_path=self.get_custom_config_path()

        self.cf=SafeConfigParser()  # 替换默认配置
        self.cf.read(self.config_path)



    def get_custom_config_path(self):
        """获取用户定制的 config 路径"""
        path=self.cf.get('custom','config_path',self.default_config_path)
        if not path:
            path=self.default_config_path
        if not os.path.exists(path):
            raise CustomConfigNotExistException(path)
        return path



parseConfig=ParseConfig()
