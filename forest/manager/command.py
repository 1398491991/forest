#coding=utf-8
from ..manager.slave_info import slaveInfoManager # 本地的
from ..command import Commander
import config
import logging

DEFAULT_SSH_LOG_CONFIG=config.DEFAULT_SSH_LOG_CONFIG

class CommandManager(object):

    def get_client_config_from_redis(self):
        pass

    def get_client_config_from_config(self):
        pass

    def get_commander(self,hostname,client_config=None,log_config=None):
        if hostname not in slaveInfoManager.get_all_slave_names():
            raise Exception

        if not client_config:
            client_config = self.get_client_config_from_redis() or self.get_client_config_from_config()

        if not client_config:
            raise Exception

        log_config=log_config or DEFAULT_SSH_LOG_CONFIG
        if log_config:
            log_config['level']=logging.getLevelName(log_config['level'])
        else:# 警告
            pass

        return Commander(client_config,log_config)




