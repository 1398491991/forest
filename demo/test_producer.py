#coding=utf-8
import sys
sys.path.append('/mnt/hgfs/project/')
sys.path.append('/mnt/hgfs/project/forest')
from forest.worker.producer import Producer
if __name__ == '__main__':

    p=Producer()
    p.start()