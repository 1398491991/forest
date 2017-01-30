#coding=utf-8
# import sys
# sys.path.append('/mnt/hgfs/project/')
# sys.path.append('/mnt/hgfs/project/forest')
from forest.worker.job import JobRequestProcess,JobItemProcess
# from forest.utils.parse_config import parseConfig
# import os
# import sys
#
# sys.path.append(os.path.dirname(parseConfig.config_path))
if __name__ == '__main__':

    job1=JobRequestProcess()

    job2=JobItemProcess()
    job1.start()
    job2.start()
    # job2.join()