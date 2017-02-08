
import paramiko
from paramiko.util import log_to_file
import logging
import forest_config


DEFAULT_SSH_LOG_CONFIG=forest_config.DEFAULT_SSH_LOG_CONFIG

class Commander(object):
    def __init__(self,client_config,log_config):
        log_to_file(**log_config)
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**client_config)
        self.ssh=ssh

    def exec_command(self,command,**kwargs):
        return self.ssh.exec_command(command,**kwargs)

    def close(self):
        return self.ssh.close()