import paramiko
from paramiko.util import log_to_file
from ..config import SSH_LOG_CONFIG

class SshCommand(object):
    def __init__(self,client_config,log_config=SSH_LOG_CONFIG):
        if log_config:
            import logging
            log_config['level']=logging.getLevelName(log_config['level'])
            log_to_file(**log_config)

        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**client_config)
        self.ssh=ssh

    def exec_command(self,*args,**kwargs):
        return self.ssh.exec_command(*args,**kwargs)

    def close(self):
        return self.ssh.close()