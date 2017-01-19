#coding=utf-8
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import os

class CustomConfigNotExistException(Exception):
    def __init__(self,path):
        self.path=path

    def __repr__(self):
        return 'config "%s" not exist'%self.path

    __str__=__repr__


class Config(object):

    # default_config_path=r'F:\forest\forest\config.ini'
    default_config_path='/mnt/hgfs/project/forest/forest/config.ini'

    def __init__(self):
        self.cf=SafeConfigParser()
        self.cf.read(self.default_config_path)

        self.config_path=self.get_custom_config_path()

        self.cf=SafeConfigParser()  # 替换默认配置
        self.cf.read(self.config_path)



    def get_custom_config_path(self):
        """获取用户定制的 config 路径"""
        path=self.get('custom','config_path',self.default_config_path)
        if not path:
            path=self.default_config_path
        if not os.path.exists(path):
            raise CustomConfigNotExistException(path)
        return path

    def _get_any(self,method ,section, option, default):
        try:
            return method(section, option)
        except (NoSectionError, NoOptionError):
            if default is not None:
                return default
            raise

    def get(self, section,option ,default=None):
        return self._get_any(self.cf.get, section,option, default)

    def getint(self,section, option, default=None):
        return self._get_any(self.cf.getint, section,option, default)

    def getfloat(self,section, option, default=None):
        return self._get_any(self.cf.getfloat,section, option, default)

    def getboolean(self,section, option, default=None):
        return self._get_any(self.cf.getboolean, section,option, default)


config=Config()