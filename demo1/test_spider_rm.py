#coding=utf-8
import sys
sys.path.append('/mnt/hgfs/project/forest/')
sys.path.append('/mnt/hgfs/forest/')
sys.path.append('d:/forest/')

from forest.services.remove import RemoveSpider

rm=RemoveSpider('test')
rm.remove()
rm.commit()


