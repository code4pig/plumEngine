# -*- coding: utf8 -*-
import script.dbproxy.object_factory as ModObjFac
import script.dbproxy.db_define as ModConf

'''
需要成为rpc目标的类必须继承于此
'''

class IDbsRpcTarget(object):
    # client通过rcp执行target的方法的时候， 执行的channel
    def GetRpcChannel(self):
        return ModConf.DBS.RPC_CHANNEL.MID_LEVEL

    def GetRpcThreadType(self):
        return ModConf.DBS.THREAD_TYPE.DEFAULT

        # 添加一个local job到rpc执行的thread， 保证local job和rpc调用在同一个线程， 确保数据安全。

    def AddJob2RpcThread(self, func, *args):
        ModObjFac.CreateApp().GetQueryRpcMgr().PushLocalJob(self.GetRpcChannel(), self.GetRpcThreadType(), func, args)


class IHiLvDbsRpcTarget(IDbsRpcTarget):
    def GetRpcChannel(self):
        return ModConf.DBS.RPC_CHANNEL.HI_LEVEL
