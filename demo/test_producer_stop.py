#coding=utf-8
import sys
sys.path.append('/mnt/hgfs/forest/')
sys.path.append('d:/forest/')


if __name__ == '__main__':
    from forest.manager.slave_status import slaveStatusItemManager,slaveStatusRequestManager
    # slaveStatusItemManager.start()
    # slaveStatusRequestManager.start()

    # slaveStatusItemManager.close()
    # slaveStatusRequestManager.kill('13528')
    # slaveStatusRequestManager.kill('15032')
    print slaveStatusRequestManager.close()