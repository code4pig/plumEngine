# -*- coding: utf8 -*-

import game
import script.dbproxy.object_factory as ModObjFac
from script.dbproxy.thread.job import CRpcJob, CLocalJob


class CQueryRpcMgr(object):
    def __init__(self):
        pass

    def PushRpcJob(self, queryRpcMsg, connid):
        try:
            job = CRpcJob(queryRpcMsg, connid)
            threadPool = ModObjFac.CreateApp().GetThreadPool(queryRpcMsg.GetTargetThreadType())
            threadPool.DispatcherJob(job, queryRpcMsg.GetTargetChannel())
        except:
            print "PushRpcJob failed!  queryRpcMsg : %s " % queryRpcMsg
            print queryRpcMsg.mt, queryRpcMsg.ma
            raise

    def PushLocalJob(self, rpcChannel, rpcThreadType, func, args):
        job = CLocalJob(func, args)
        threadPool = ModObjFac.CreateApp().GetThreadPool(rpcThreadType)
        threadPool.DispatcherJob(job, rpcChannel)
