#coding=utf-8

from forest.utils.misc import get_host_name

if __name__ == '__main__':
    from forest.manager.slave_status import slaveStatusItemManager,slaveStatusRequestManager
    # slaveStatusItemManager.start()
    # slaveStatusRequestManager.start()

    # slaveStatusItemManager.close()
    print slaveStatusRequestManager.close()