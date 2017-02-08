#coding=utf-8


from forest.spider.info import GetSpiderInfo,SetSpiderInfo,RemoveSpiderInfo

getSpiderInfo=GetSpiderInfo(transaction=True)
getSpiderInfo.rd_server.set('test_info','test')
getSpiderInfo.execute(True)
getSpiderInfo.transaction=False # 更换事物状态
getSpiderInfo.rd_server.delete('test_info')
